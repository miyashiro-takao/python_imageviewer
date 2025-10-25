from __future__ import annotations

"""UI for managing destination folders used by the image viewer."""

from importlib import resources
from pathlib import Path
from tkinter import filedialog

import tkinter as tk
from PIL import Image, ImageTk

from .configuration import (
    get_config,
    get_folder_settings,
    normalise_path,
    save_config as save_config_to_disk,
)


class ImageGrouping(tk.Frame):
    """Display selectable folders and persist the user's choices."""

    LABEL_PADDING = {"padx": 0, "pady": 0}

    def __init__(self, master=None):
        super().__init__(master)

        self._config_data = get_config()
        folder_paths, self.icon_size = get_folder_settings()
        if not folder_paths:
            folder_paths = [""] * 4

        self.folder_path_vars = [tk.StringVar(value=path) for path in folder_paths]
        self.folder_name_vars = [
            tk.StringVar(value=Path(path).name if path else "") for path in folder_paths
        ]

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Create folder icons and labels."""
        icon_image = self._load_icon()
        icon_tk = ImageTk.PhotoImage(icon_image)

        for index, _ in enumerate(self.folder_path_vars):
            label = tk.Label(self, image=icon_tk)
            label.image = icon_tk
            label.grid(row=0, column=index, **self.LABEL_PADDING)
            label.bind("<Button-1>", lambda event, idx=index: self.open_folder_dialog(idx))

            folder_name_label = tk.Label(self, textvariable=self.folder_name_vars[index])
            folder_name_label.grid(row=1, column=index, **self.LABEL_PADDING)

        placeholder = tk.Label(self)
        placeholder.grid(
            row=2, column=0, columnspan=len(self.folder_path_vars), padx=5, pady=10
        )

    def _load_icon(self) -> Image.Image:
        """Load the bundled icon and resize it according to the config."""
        icon_path = resources.files(__package__) / "assets" / "icon.png"
        with icon_path.open("rb") as icon_file:
            with Image.open(icon_file) as image:
                return image.copy().resize(self.icon_size, Image.LANCZOS)

    def _update_config_from_vars(self) -> None:
        """Synchronise Tk variables back to the configuration dictionary."""
        folders_section = self._config_data.setdefault("folders", {})
        folder_paths = folders_section.setdefault("paths", [])
        if len(folder_paths) < len(self.folder_path_vars):
            folder_paths.extend("" for _ in range(len(self.folder_path_vars) - len(folder_paths)))

        for index, var in enumerate(self.folder_path_vars):
            normalised = normalise_path(var.get())
            folder_paths[index] = normalised
            self.folder_path_vars[index].set(normalised)

    def open_folder_dialog(self, index: int) -> None:
        """Open a folder picker and persist the selected location."""
        selected_folder = filedialog.askdirectory()
        if not selected_folder:
            return

        folder_path = Path(selected_folder)
        normalised_path = normalise_path(str(folder_path))
        self.folder_path_vars[index].set(normalised_path)
        self.folder_name_vars[index].set(folder_path.name)

        self._update_config_from_vars()
        save_config_to_disk(self._config_data)

    def save_config(self) -> None:
        """Save the current folder settings to disk."""
        self._update_config_from_vars()
        save_config_to_disk(self._config_data)
