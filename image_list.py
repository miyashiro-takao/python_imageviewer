import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import math
import datetime
from image_display import ImageDisplay

class ImageList(tk.Frame):
    def __init__(self, master=None, current_image_path=None, image_display=None):
        super().__init__(master)
        self.image_display = image_display
        self.current_image_path = current_image_path if current_image_path is not None else [None] # current_image_path を初期化
        self.create_widgets() # create_widgets 関数を呼び出す


    # Treeviewのウィジェットを作成する関数
    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=("filename", "size", "ratio", "ext", "created", "fullpath"), selectmode="browse", show="headings")
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
        self.tree.heading("fullpath", text="フルパス")
        self.tree.column("fullpath", anchor=tk.CENTER, width=0)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.bind("<Up>", self.select_previous_image)
        self.bind("<Down>", self.select_next_image)

        self.tree.bind("<<TreeviewSelect>>", self.on_treeview_select)

        self.tree.focus_set()  # Treeviewウィジェットにフォーカスを設定
        self.tree.bind("<FocusIn>", self.on_treeview_focus)

        self.tree.focus_set()
        focused_widget = self.focus_get()
        print(f"Focused widget: {focused_widget}")
        focused_widget = self.tree.focus_get()
        print(f"Focused widget: {focused_widget}")

    # 指定されたフォルダパス内の画像ファイル情報をTreeviewに追加するメソッド
    def populate_treeview(self, folder_path):
        self.tree.delete(*self.tree.get_children())
        self.current_folder = folder_path
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_path = file_path.replace('\\', '/')
                filename, ext = os.path.splitext(file)
                ext = ext.lower()
                if ext in {".jpg", ".jpeg", ".png", ".gif"}:
                    img = Image.open(file_path)
                    width, height = img.size
                    size = f"{width} x {height}"
                    gcd = math.gcd(width, height)
                    ratio = f"{width//gcd} : {height//gcd}"
                    created_timestamp = os.path.getctime(file_path)
                    created_dt = datetime.datetime.fromtimestamp(created_timestamp)
                    created = created_dt.strftime("%Y/%m/%d %H:%M").replace(" 0", " ")
                    self.tree.insert("", "end", text="", values=(file, size, ratio, ext, created, file_path))
        # 一番上の画像を選択する
        if self.tree.exists('I001'):  # 一番上の画像が存在するかどうかを確認
            self.tree.selection_set('I001')  # 一番上の画像を選択
            self.tree.focus_set()
            self.tree.focus('I001')  # Treeviewウィジェットにフォーカスを設定
            self.tree.see('I001')  # 一番上の画像が表示されるようにスクロール



    # Treeviewで選択された画像を表示する関数
    def on_treeview_select(self, event=None):
        selected_item = self.tree.selection()[0]  # 選択されたアイテムを取得
        file_path = self.tree.item(selected_item, "values")[5]  # 選択されたアイテムのフルパスを取得
        if self.image_display:  # 画像表示オブジェクトが存在する場合
            self.image_display.load_image(file_path)  # 画像表示エリアに選択された画像を表示

    # Treeviewの子要素を取得し、指定されたカラムの値に基づいてリストに変換
    def treeview_sort_column(self, col, reverse):
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        l.sort(reverse=reverse)  # リストを並べ替え

        # 並べ替えたリストに基づいて、Treeviewの要素を並び替え
        for index, (_, k) in enumerate(l):
            self.tree.move(k, "", index)

        # カラムのヘッダーをクリックしたときに、逆順に並べ替えるようにコマンドを設定
        self.tree.heading(col, command=lambda: self.treeview_sort_column(col, not reverse))

    # 選択されているアイテムの前のアイテムを選択する
    def select_previous_image(self, event):
        print("Up key pressed")  # デバッグメッセージを追加
        selected_item = self.tree.selection()
        if not selected_item:
            return
        prev_item = self.tree.prev(selected_item[0])
        if prev_item:
            self.tree.selection_set(prev_item)
            self.tree.focus(prev_item)
            self.on_treeview_select(None)

    # 選択されているアイテムの次のアイテムを選択する
    def select_next_image(self, event):
        print("Down key pressed")  # デバッグメッセージを追加
        selected_item = self.tree.selection()
        if not selected_item:
            return
        next_item = self.tree.next(selected_item[0])
        if next_item:
            self.tree.selection_set(next_item)
            self.tree.focus(next_item)
            self.on_treeview_select(None)

    def on_treeview_focus(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            item_path = self.tree.item(selected_item)['values'][1]

            if os.path.isfile(item_path):
                self.image_display.update_image(item_path)
            else:
                children = self.tree.get_children()
                if children:
                    first_item = children[0]
                    self.tree.selection_set(first_item)
                    self.tree.focus(first_item)