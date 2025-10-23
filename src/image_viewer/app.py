"""画像ビューアアプリ全体のウィンドウ構成を定義するモジュール。"""

from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, ttk

from .image_display import ImageDisplay
from .image_grouping import ImageGrouping
from .image_list import ImageList
from .key_events import KeyEvents


class ViewerWindow(tk.Tk):
    """アプリ全体のメインウィンドウ。"""

    DEFAULT_GEOMETRY = "800x600"
    TITLE = "画像分類アプリ"

    def __init__(self) -> None:
        super().__init__()

        self.title(self.TITLE)
        self.geometry(self.DEFAULT_GEOMETRY)

        self.image_display: ImageDisplay | None = None
        self.image_list: ImageList | None = None
        self.image_grouping: ImageGrouping | None = None
        self.key_events: KeyEvents | None = None

        self._build_ui()
        self._configure_bindings()

    def _build_ui(self) -> None:
        """ウィンドウ内の全ての領域を初期化する。"""
        self._build_menu()
        self._build_separators()
        self._build_image_display()
        self._build_image_list()
        self._build_image_grouping()

    def _build_menu(self) -> None:
        """メニューバーとファイルメニューを生成する。"""
        menu_bar = tk.Menu(self)

        file_menu = tk.Menu(menu_bar, tearoff=False)
        file_menu.add_command(label="開く", command=self.open_folder_dialog)
        file_menu.add_separator()
        file_menu.add_command(label="終了", command=self.quit)
        menu_bar.add_cascade(label="ファイル", menu=file_menu)

        self.config(menu=menu_bar)

    def _build_separators(self) -> None:
        """一覧・表示・分類の領域を視覚的に区切る。"""
        separator_vertical = ttk.Separator(self, orient="vertical")
        separator_vertical.place(relx=0.5, rely=0, relheight=2, anchor="center")

        separator_horizontal = ttk.Separator(self, orient="horizontal")
        separator_horizontal.place(relx=0, rely=0.8, relwidth=0.5, anchor="nw")

    def _build_image_display(self) -> None:
        """右側の画像表示領域を構築する。"""
        self.image_display = ImageDisplay(self)
        self.image_display.place(relx=0.5, rely=0, relwidth=0.5, relheight=1, anchor="nw")

    def _build_image_list(self) -> None:
        """左上の画像一覧領域を構築する。"""
        self.image_list = ImageList(self, image_display=self.image_display)
        self.image_list.place(rely=0, relx=0, relwidth=0.5, relheight=0.8, anchor="nw")

    def _build_image_grouping(self) -> None:
        """左下の分類フォルダ設定領域を構築する。"""
        self.image_grouping = ImageGrouping(self)
        self.image_grouping.place(relx=0, rely=0.8, relwidth=0.5, relheight=0.2, anchor="nw")

    def _configure_bindings(self) -> None:
        """ウィンドウ全体に必要なイベントバインドを設定する。"""
        self.bind("<F1>", self.print_focused_widget)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.key_events = KeyEvents(self, self.image_display, self.image_list)
        self.bind_all("z", lambda event: self._move_to_folder(0))

    def _move_to_folder(self, folder_index: int) -> None:
        """ショートカットから分類フォルダへ移動する。"""
        if self.image_list and self.image_grouping:
            self.image_list.move_image(folder_index, self.image_grouping.folder_path_vars)

    def open_folder_dialog(self) -> None:
        """フォルダ選択ダイアログを開き、一覧を読み込む。"""
        folder_path = filedialog.askdirectory()
        if folder_path and self.image_list:
            self.image_list.populate_treeview(folder_path)

    def on_closing(self) -> None:
        """ウィンドウを閉じる前に設定を保存する。"""
        if self.image_grouping:
            self.image_grouping.save_config()
        self.destroy()

    def print_focused_widget(self, event=None) -> None:
        """現在フォーカスされているウィジェット情報を出力する。"""
        widget = self.focus_get()
        if widget:
            print(f"Focused widget: {widget}")
        elif self.image_list:
            print("No focused widget. Setting focus to Treeview.")
            self.image_list.tree.focus_set()


def run() -> None:
    """アプリケーションを起動するエントリーポイント。"""
    app = ViewerWindow()
    app.mainloop()
