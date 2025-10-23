"""キーボードショートカットをまとめて管理するモジュール。"""

import tkinter as tk


class KeyEvents:
    """ビュー全体に対するキーイベントを束ねるヘルパー。"""

    def __init__(self, parent: tk.Tk, image_display, image_list):
        self.parent = parent
        self.image_display = image_display
        self.image_list = image_list
        self.bind_key_events()

    def bind_key_events(self) -> None:
        """主要なショートカットキーをウィンドウに登録する。"""
        self.parent.bind("<space>", lambda event: self.parent.open_folder_dialog())
        self.parent.bind("<Escape>", lambda event: self.parent.destroy())
        self.parent.bind("<Up>", self.previous_image)
        self.parent.bind("<Down>", self.next_image)

    def previous_image(self, event=None) -> None:
        """一覧の一つ前の項目へ移動する。"""
        if self.image_list is not None:
            self.image_list.select_previous_image(event)

    def next_image(self, event=None) -> None:
        """一覧の一つ後ろの項目へ移動する。"""
        if self.image_list is not None:
            self.image_list.select_next_image(event)
