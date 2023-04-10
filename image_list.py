import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import math
import datetime

class ImageList(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.current_folder = ""
        self.create_widgets()

        # WキーとSキーで画像一覧の表示を切り替えるキーバインディングを設定
        self.tree.bind('w', self.select_previous_image)
        self.tree.bind('W', self.select_previous_image)
        self.tree.bind('s', self.select_next_image)
        self.tree.bind('S', self.select_next_image)


    # ウィジェットを作成する関数
    def create_widgets(self):
        # Treeviewの設定
        self.tree = ttk.Treeview(self, columns=("filename", "size", "ratio", "ext", "created"), selectmode="browse", show="headings")
        self.tree.heading("filename", text="ファイル名", command=lambda: self.treeview_sort_column("filename", False))
        self.tree.column("filename", anchor=tk.W, width=200)
        self.tree.heading("size", text="サイズ", command=lambda: self.treeview_sort_column("size", False))
        self.tree.column("size", anchor=tk.CENTER, width=80)
        self.tree.heading("ratio", text="縦横比", command=lambda: self.treeview_sort_column("ratio", False))
        self.tree.column("ratio", anchor=tk.CENTER, width=50)
        self.tree.heading("ext", text="拡張子", command=lambda: self.treeview_sort_column("ext", False))
        self.tree.column("ext", anchor=tk.CENTER, width=50)
        self.tree.heading("created", text="作成日", command=lambda: self.treeview_sort_column("created", False))
        self.tree.column("created", anchor=tk.CENTER, width=100)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_treeview_select)

    # Treeviewに画像情報を追加する関数
    def populate_treeview(self, folder_path):
        self.tree.delete(*self.tree.get_children())
        self.current_folder = folder_path
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                filename, ext = os.path.splitext(file)
                ext = ext.lower()
                if ext in {".jpg", ".jpeg", ".png", ".gif"}:
                    img = Image.open(file_path)
                    width, height = img.size
                    size = f"{width} x {height}"
                    gcd = math.gcd(width, height)  # 最大公約数を求める
                    ratio = f"{width//gcd} : {height//gcd}"  # 縦横比を整数の比率で表示
                    created_timestamp = os.path.getctime(file_path)  # タイムスタンプを取得
                    created_dt = datetime.datetime.fromtimestamp(created_timestamp)  # タイムスタンプを datetime オブジェクトに変換
                    created = created_dt.strftime("%Y/%m/%d %H:%M").replace(" 0", " ")
                    self.tree.insert("", "end", text="", values=(file, size, ratio, ext, created))

    # Treeviewで選択された画像を表示する関数
    def on_treeview_select(self, event):
        selected_item = self.tree.selection()[0]  # 選択されたアイテムを取得
        filename = self.tree.item(selected_item)["values"][0]  # 選択されたアイテムのファイル名を取得
        file_path = os.path.join(self.current_folder, filename)  # ファイル名からファイルパスを作成
        if os.path.isfile(file_path):  # ファイルパスがファイルを指している場合
            self.parent.image_display.load_image(file_path)  # 画像を読み込む
        
    def treeview_sort_column(self, col, reverse):
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        l.sort(reverse=reverse)

        for index, (_, k) in enumerate(l):
            self.tree.move(k, "", index)

        self.tree.heading(col, command=lambda: self.treeview_sort_column(col, not reverse))

    def select_previous_image(self, event=None):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        prev_item = self.tree.prev(selected_item[0])
        if prev_item:
            self.tree.selection_set(prev_item)
            self.tree.focus(prev_item)
            self.on_treeview_select(None)

    def select_next_image(self, event=None):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        next_item = self.tree.next(selected_item[0])
        if next_item:
            self.tree.selection_set(next_item)
            self.tree.focus(next_item)
            self.on_treeview_select(None)
