"""画像一覧を管理し、選択に応じて表示を更新するモジュール。"""

from __future__ import annotations

import datetime
import math
import shutil
import tkinter as tk
from pathlib import Path
from tkinter import ttk

from PIL import Image

from .configuration import get_supported_extensions


class ImageList(tk.Frame):
    """画像ファイルの一覧表示とナビゲーションを担当するフレーム。"""

    def __init__(self, master=None, image_display=None) -> None:
        super().__init__(master)
        self.image_display = image_display
        self.current_folder: Path | None = None

        self.tree = self._build_tree()
        self._configure_bindings()

    def _build_tree(self) -> ttk.Treeview:
        """一覧用の Treeview とスクロールバーを構築する。"""
        tree = ttk.Treeview(
            self,
            columns=("filename", "size", "ratio", "ext", "created", "fullpath"),
            selectmode="browse",
            show="headings",
        )
        tree.heading("filename", text="ファイル名", command=lambda: self._sort_by("filename"))
        tree.column("filename", anchor=tk.W, width=200)

        tree.heading("size", text="サイズ", command=lambda: self._sort_by("size"))
        tree.column("size", anchor=tk.CENTER, width=80)

        tree.heading("ratio", text="縦横比", command=lambda: self._sort_by("ratio"))
        tree.column("ratio", anchor=tk.CENTER, width=50)

        tree.heading("ext", text="拡張子", command=lambda: self._sort_by("ext"))
        tree.column("ext", anchor=tk.CENTER, width=50)

        tree.heading("created", text="作成日", command=lambda: self._sort_by("created"))
        tree.column("created", anchor=tk.CENTER, width=120)

        tree.heading("fullpath", text="フルパス")
        tree.column("fullpath", anchor=tk.CENTER, width=0, stretch=False)

        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=scrollbar.set)

        return tree

    def _configure_bindings(self) -> None:
        """Treeview に必要なイベントをバインドする。"""
        self.tree.bind("<<TreeviewSelect>>", self.on_treeview_select)
        self.tree.bind("<FocusIn>", self._ensure_selection)

    def populate_treeview(self, folder_path: str | Path) -> None:
        """指定フォルダから画像を読み込み、一覧へ反映する。"""
        folder = Path(folder_path)
        if not folder.exists():
            return

        self.tree.delete(*self.tree.get_children())
        self.current_folder = folder

        supported_extensions = {ext.lower() for ext in get_supported_extensions()}

        for file_path in sorted(folder.rglob("*")):
            if file_path.suffix.lower() not in supported_extensions:
                continue

            with Image.open(file_path) as img:
                width, height = img.size

            gcd_value = math.gcd(width, height)
            ratio = f"{width // gcd_value}:{height // gcd_value}"
            size_text = f"{width} x {height}"

            created_timestamp = file_path.stat().st_ctime
            created_dt = datetime.datetime.fromtimestamp(created_timestamp)
            created_text = created_dt.strftime("%Y/%m/%d %H:%M")

            self.tree.insert(
                "",
                "end",
                values=(
                    file_path.name,
                    size_text,
                    ratio,
                    file_path.suffix.lower(),
                    created_text,
                    str(file_path),
                ),
            )

        first_item = self._first_tree_item()
        if first_item:
            self.tree.selection_set(first_item)
            self.tree.focus(first_item)
            self.tree.see(first_item)

    def on_treeview_select(self, event=None) -> None:
        """選択行のファイルを ImageDisplay に渡す。"""
        selection = self.tree.selection()
        if not selection:
            return

        full_path = Path(self.tree.item(selection[0], "values")[5])
        if self.image_display:
            self.image_display.load_image(full_path)

    def _sort_by(self, column: str, reverse: bool = False) -> None:
        """指定カラムで一覧を並び替える。"""
        rows = [(self.tree.set(item, column), item) for item in self.tree.get_children("")]
        rows.sort(reverse=reverse)

        for index, (_, item) in enumerate(rows):
            self.tree.move(item, "", index)

        self.tree.heading(column, command=lambda: self._sort_by(column, not reverse))

    def select_previous_image(self, event=None) -> None:
        """一つ前の項目を選択し直す。"""
        selection = self.tree.selection()
        if not selection:
            return

        previous_item = self.tree.prev(selection[0])
        if previous_item:
            self.tree.selection_set(previous_item)
            self.tree.focus(previous_item)
            self.tree.see(previous_item)
            self.on_treeview_select()

    def select_next_image(self, event=None) -> None:
        """一つ後ろの項目を選択し直す。"""
        selection = self.tree.selection()
        if not selection:
            return

        next_item = self.tree.next(selection[0])
        if next_item:
            self.tree.selection_set(next_item)
            self.tree.focus(next_item)
            self.tree.see(next_item)
            self.on_treeview_select()

    def _ensure_selection(self, event=None) -> None:
        """Treeview にフォーカスが戻った際に最初の行を選択させる。"""
        if not self.tree.selection():
            first_item = self._first_tree_item()
            if first_item:
                self.tree.selection_set(first_item)
                self.tree.focus(first_item)

    def _first_tree_item(self) -> str | None:
        """Treeview の先頭項目 ID を返す。"""
        children = self.tree.get_children()
        return children[0] if children else None

    def move_image(self, index: int, folder_path_vars) -> None:
        """選択中の画像を指定フォルダへ移動し、一覧から削除する。"""
        selection = self.tree.selection()
        if not selection:
            return

        full_path = Path(self.tree.item(selection[0], "values")[5])
        if index >= len(folder_path_vars):
            return

        destination_folder = Path(folder_path_vars[index].get())

        if not destination_folder:
            return

        destination_folder.mkdir(parents=True, exist_ok=True)
        destination_path = destination_folder / full_path.name
        shutil.move(str(full_path), str(destination_path))

        next_item = self.tree.next(selection[0])
        self.tree.delete(selection[0])

        if next_item:
            self.tree.selection_set(next_item)
            self.tree.focus(next_item)
            self.tree.see(next_item)
            self.on_treeview_select()
