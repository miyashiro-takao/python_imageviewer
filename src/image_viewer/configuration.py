from __future__ import annotations

import copy
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

try:
    import tomllib  # type: ignore[attr-defined]
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore[no-redef]

import configparser

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_FILENAME = "config.toml"
CONFIG_PATH = PROJECT_ROOT / CONFIG_FILENAME
LEGACY_CONFIG_PATH = PROJECT_ROOT / "config.ini"

DEFAULT_CONFIG: dict[str, Any] = {
    "folders": {
        "paths": ["", "", "", ""],
        "icon_size": [64, 64],
    },
    "viewer": {
        "title": "画像分類アプリ",
        "default_geometry": "800x600",
        "last_opened_directory": "",
    },
    "images": {
        "supported_extensions": [".jpg", ".jpeg", ".png", ".gif"],
    },
}


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge two dictionaries, returning a new structure."""
    result: dict[str, Any] = {}
    keys = set(base) | set(override)
    for key in keys:
        base_value = base.get(key)
        override_value = override.get(key)
        if isinstance(base_value, dict) and isinstance(override_value, dict):
            result[key] = _deep_merge(base_value, override_value)
        elif override_value is not None:
            result[key] = copy.deepcopy(override_value)
        else:
            result[key] = copy.deepcopy(base_value)
    return result


def _dump_array(key: str, values: Iterable[Any]) -> list[str]:
    """Format a Python iterable as a TOML array line sequence."""
    json_lines = json.dumps(list(values), ensure_ascii=False, indent=4).splitlines()
    if not json_lines:
        return [f"{key} = []"]

    lines = [f"{key} = {json_lines[0]}"]
    if len(json_lines) > 1:
        lines.extend(json_lines[1:])
    return lines


def _build_config_text(config: dict[str, Any]) -> str:
    """Build the TOML text with explanatory comments."""
    lines: list[str] = [
        "# 画像ビューアの設定ファイル (TOML)",
        "# 数値や文字列の調整はここで行います。",
        "",
        "# 画像を分類する際に使用するフォルダパス一覧。",
        "# 表示順に意味がある場合は並び替えてください。",
        "[folders]",
    ]

    lines.extend(_dump_array("paths", config["folders"].get("paths", [])))
    lines.append("")
    lines.append("# アイコンの表示サイズ [幅, 高さ]")
    lines.extend(_dump_array("icon_size", config["folders"].get("icon_size", [])))
    lines.append("")

    lines.append("# アプリケーションウィンドウの見た目に関する設定。")
    lines.append("[viewer]")
    lines.append(f"title = {json.dumps(config['viewer'].get('title', ''), ensure_ascii=False)}")
    lines.append(f"default_geometry = {json.dumps(config['viewer'].get('default_geometry', ''), ensure_ascii=False)}")
    lines.append("# アプリを再起動した際に自動で開くフォルダ。空文字にすると無効化。")
    lines.append(
        f"last_opened_directory = {json.dumps(config['viewer'].get('last_opened_directory', ''), ensure_ascii=False)}"
    )
    lines.append("")

    lines.append("# 一覧表示で扱う画像ファイルの拡張子。小文字で指定してください。")
    lines.append("[images]")
    lines.extend(_dump_array("supported_extensions", config["images"].get("supported_extensions", [])))
    lines.append("")

    return "\n".join(lines)


def _load_legacy_ini() -> dict[str, Any]:
    """Load folder configuration from the legacy INI file for migration."""
    parser = configparser.ConfigParser()
    parser.read(LEGACY_CONFIG_PATH, encoding="utf-8")

    folder_paths: list[str] = []
    if parser.has_section("folders"):
        # Sort keys like folder0, folder1, ...
        items = sorted(parser.items("folders"), key=lambda item: item[0])
        folder_paths.extend(value.strip() for _, value in items)

    if not folder_paths:
        return copy.deepcopy(DEFAULT_CONFIG)

    merged = copy.deepcopy(DEFAULT_CONFIG)
    merged["folders"]["paths"] = [_normalise_path_string(path) for path in folder_paths]
    return merged


def _normalise_path_string(path: str) -> str:
    """Convert Windows-style backslashes to forward slashes for TOML safety."""
    return path.replace("\\", "/")


def _normalise_config_paths(config: dict[str, Any]) -> dict[str, Any]:
    """Ensure all path strings use forward slashes before writing."""
    folders_section = config.get("folders", {})
    paths = folders_section.get("paths", [])
    if isinstance(paths, list):
        folders_section["paths"] = [
            _normalise_path_string(path) if isinstance(path, str) else path for path in paths
        ]

    viewer_section = config.get("viewer", {})
    last_dir = viewer_section.get("last_opened_directory", "")
    if isinstance(last_dir, str):
        viewer_section["last_opened_directory"] = _normalise_path_string(last_dir)

    return config


@dataclass(slots=True)
class ConfigManager:
    """Centralised access to the application configuration."""

    config_path: Path = CONFIG_PATH
    legacy_config_path: Path = LEGACY_CONFIG_PATH
    _config_cache: dict[str, Any] | None = None

    def load(self) -> dict[str, Any]:
        """Load configuration, reading from disk once and caching results."""
        if self._config_cache is None:
            self._config_cache = self._load_from_disk()
        return copy.deepcopy(self._config_cache)

    def save(self, config: dict[str, Any]) -> None:
        """Persist configuration to disk and update the cache."""
        merged = _deep_merge(DEFAULT_CONFIG, config)
        self._config_cache = copy.deepcopy(merged)
        self._write_file(merged)

    def _load_from_disk(self) -> dict[str, Any]:
        if self.config_path.exists():
            try:
                with self.config_path.open("rb") as file:
                    loaded = tomllib.load(file)
            except tomllib.TOMLDecodeError:
                print("Failed to parse config.toml; recreating it with defaults.")
                loaded = {}
            merged = _deep_merge(DEFAULT_CONFIG, loaded)
        elif self.legacy_config_path.exists():
            merged = _load_legacy_ini()
        else:
            merged = copy.deepcopy(DEFAULT_CONFIG)

        # Ensure the TOML file exists with comments for first-time users.
        if not self.config_path.exists():
            self._write_file(merged)
        else:
            # Normalise any paths that may still contain backslashes.
            merged = _normalise_config_paths(merged)
            self._write_file(merged)

        return merged

    def _write_file(self, config: dict[str, Any]) -> None:
        normalised = _normalise_config_paths(copy.deepcopy(config))
        text = _build_config_text(normalised)
        self.config_path.write_text(text, encoding="utf-8")


_manager = ConfigManager()


def get_config() -> dict[str, Any]:
    """Return a copy of the current configuration."""
    return _manager.load()


def save_config(config: dict[str, Any]) -> None:
    """Persist configuration updates."""
    _manager.save(config)


def get_supported_extensions() -> list[str]:
    """Convenience accessor for supported image extensions."""
    config = _manager.load()
    extensions = config["images"].get("supported_extensions", [])
    return [ext.lower() for ext in extensions]


def get_folder_settings() -> tuple[list[str], tuple[int, int]]:
    """Return folder paths and icon size settings."""
    config = _manager.load()
    raw_paths = config["folders"].get("paths", [])
    folder_paths = [
        _normalise_path_string(path) if isinstance(path, str) else path for path in raw_paths
    ]
    icon_size_values = config["folders"].get("icon_size", [64, 64])
    icon_size = tuple(int(value) for value in icon_size_values[:2])
    if len(icon_size) != 2:
        icon_size = (64, 64)
    return folder_paths, icon_size


def get_last_opened_directory() -> str:
    """Return the last folder opened in the viewer, if any."""
    config = _manager.load()
    last_dir = config.get("viewer", {}).get("last_opened_directory", "")
    if isinstance(last_dir, str):
        return _normalise_path_string(last_dir)
    return ""


def set_last_opened_directory(path: str) -> None:
    """Persist the directory that should open on startup."""
    config = _manager.load()
    viewer_config = config.setdefault("viewer", {})
    viewer_config["last_opened_directory"] = _normalise_path_string(path)
    save_config(config)


def normalise_path(path: str) -> str:
    """Public helper primarily for UI components to store safe path strings."""
    return _normalise_path_string(path)
