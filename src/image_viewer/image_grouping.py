from __future__ import annotations

"""分類フォルダの設定と表示を扱うモジュール。"""

import configparser
from importlib import resources
from pathlib import Path
from tkinter import filedialog

import tkinter as tk
from PIL import Image, ImageTk

CONFIG_FILENAME = "config.ini"


class ImageGrouping(tk.Frame):
    """画像を振り分けるフォルダ設定とUIをまとめたフレーム。"""

    ICON_SIZE = (64, 64)
    LABEL_PADDING = {"padx": 0, "pady": 0}
    SECTION_FOLDERS = "folders"

    def __init__(self, master=None):
        super().__init__(master)

        self.folder_name_vars = [tk.StringVar() for _ in range(4)]
        self.folder_path_vars = [tk.StringVar() for _ in range(4)]

        self.config = configparser.ConfigParser()
        self._load_config()
        self._setup_ui()

    def _setup_ui(self) -> None:
        """フォルダアイコンとラベルを並べて配置する。"""
        icon_image = self._load_icon()
        icon_tk = ImageTk.PhotoImage(icon_image)

        for index in range(4):
            label = tk.Label(self, image=icon_tk)
            label.image = icon_tk
            label.grid(row=0, column=index, **self.LABEL_PADDING)
            label.bind("<Button-1>", lambda event, idx=index: self.open_folder_dialog(self.folder_path_vars[idx], idx))

            folder_name_label = tk.Label(self, textvariable=self.folder_name_vars[index])
            folder_name_label.grid(row=1, column=index, **self.LABEL_PADDING)

        placeholder = tk.Label(self)
        placeholder.grid(row=2, column=0, columnspan=4, padx=5, pady=10)

    def _load_icon(self) -> Image.Image:
        """パッケージ同梱のアイコンを読み込んでリサイズする。"""
        icon_path = resources.files(__package__) / "assets" / "icon.png"
        with icon_path.open("rb") as icon_file:
            with Image.open(icon_file) as image:
                return image.copy().resize(self.ICON_SIZE, Image.LANCZOS)

    def open_folder_dialog(self, folder_path_var: tk.StringVar, index: int) -> None:
        """フォルダ選択ダイアログを開き、選択内容を保存する。"""
        selected_folder = filedialog.askdirectory()
        if not selected_folder:
            return

        folder_path = Path(selected_folder)
        self.folder_path_vars[index].set(str(folder_path))
        self.folder_name_vars[index].set(folder_path.name)

        self.config.set(self.SECTION_FOLDERS, f"folder{index}", str(folder_path))
        self._save_config()

    def _save_config(self) -> None:
        """設定内容をINIファイルへ書き出す。"""
        with open(CONFIG_FILENAME, "w", encoding="utf-8") as configfile:
            self.config.write(configfile)

    def _load_config(self) -> None:
        """INIファイルからフォルダ設定を読み込む。"""
        config_path = Path(CONFIG_FILENAME)
        if not config_path.exists():
            config_path.write_text(self._default_config_text(), encoding="utf-8")

        self.config.read(config_path, encoding="utf-8")
        if not self.config.has_section(self.SECTION_FOLDERS):
            self.config.add_section(self.SECTION_FOLDERS)

        for index in range(4):
            option = f"folder{index}"
            if not self.config.has_option(self.SECTION_FOLDERS, option):
                self.config.set(self.SECTION_FOLDERS, option, "")

            folder_path = Path(self.config.get(self.SECTION_FOLDERS, option, fallback=""))
            self.folder_path_vars[index].set(str(folder_path))
            self.folder_name_vars[index].set(folder_path.name if folder_path.name else "")

    def _default_config_text(self) -> str:
        """初期状態の設定ファイル内容を生成する。"""
        lines = [f"[{self.SECTION_FOLDERS}]"]
        lines.extend(f"folder{index} = " for index in range(4))
        return "\n".join(lines)

    def save_config(self) -> None:
        """外部から明示的に保存したい場合のラッパー。"""
        self._save_config()
