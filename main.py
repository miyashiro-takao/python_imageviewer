import tkinter as tk
from tkinter import filedialog, ttk
from image_list import ImageList
from Image_display import ImageDisplay
from image_grouping import ImageGrouping

class ViewerWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # ウィンドウの大きさを設定
        self.geometry("800x600")
        self.title("画像分類アプリ")

        # メニューバーの作成
        self.create_menu()

        # Separatorの作成
        self.create_separators()

        # 画像一覧エリアの作成
        self.create_image_list()

        # 画像表示エリアの作成
        self.create_image_display()
 
        # 画像分類エリアの作成
        self.create_image_grouping()

        # フォルダ選択ダイアログが自動で開かれるようにする
        self.open_folder_dialog()

    # メニューバーを作成する関数
    def create_menu(self):
        menu_bar = tk.Menu(self)

        # ファイルメニュー
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="開く", command=self.open_folder_dialog)
        file_menu.add_separator()
        file_menu.add_command(label="終了", command=self.quit)

        menu_bar.add_cascade(label="ファイル", menu=file_menu)

        # メニューバーをウィンドウに配置
        self.config(menu=menu_bar)

    # Separatorを作成する関数
    def create_separators(self):
        # 縦のSeparator
        separator_vertical = ttk.Separator(self, orient='vertical')
        separator_vertical.place(relx=0.5, rely=0, relheight=2, anchor='center')

        # 横のSeparator
        separator_horizontal = ttk.Separator(self, orient='horizontal')
        separator_horizontal.place(relx=0, rely=0.8, relwidth=0.5, anchor='nw')

    # 画像一覧エリアを作成する関数
    def create_image_list(self):
        self.image_list = ImageList(self)
        self.image_list.place(rely=0, relx=0, relwidth=0.5, relheight=0.8, anchor='nw')

    # 画像表示エリアを作成する関数
    def create_image_display(self):
        self.image_display = ImageDisplay(self)
        self.image_display.place(relx=0.5, rely=0, relwidth=0.5, relheight=1, anchor='nw')

    # 画像分類エリアを作成する関数
    def create_image_grouping(self):
        self.image_grouping = ImageGrouping(self)
        self.image_grouping.place(relx=0, rely=0.8, relwidth=0.5, relheight=0.2, anchor='nw')

    # フォルダダイアログを開く関数
    def open_folder_dialog(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.image_list.populate_treeview(folder_path)
            # 一番上の画像を選択する
            first_item = self.image_list.tree.get_children()[0]
            self.image_list.tree.selection_set(first_item)
            self.image_list.tree.focus_set()
            self.image_list.tree.focus(first_item)

if __name__ == "__main__":
    app = ViewerWindow()
    app.mainloop()