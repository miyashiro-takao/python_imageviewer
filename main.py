import tkinter as tk
from tkinter import filedialog, ttk
from image_list import ImageList
from image_display import ImageDisplay
from image_grouping import ImageGrouping
from key_events import KeyEvents

class ViewerWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        # ウィンドウの大きさを設定
        self.geometry("800x600")
        self.title("画像分類アプリ")
        self.create_menu() # メニューバーの作成
        self.create_separators() # Separatorの作成
        self.create_image_display() # 画像表示エリアの作成
        self.create_image_list() # 画像一覧エリアの作成
        self.create_image_grouping() # 画像分類エリアの作成
        #self.open_folder_dialog() # フォルダ選択ダイアログが自動で開かれるようにする
        self.key_events = KeyEvents(self, self.image_display, self.image_list) # キーイベントの設定

        self.bind("<F1>", lambda event: self.print_focused_widget())  # F1 キーを押すとフォーカスされているウィジェットを表示
        self.protocol("WM_DELETE_WINDOW", self.on_closing)


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
        self.current_image_path = [""]
        self.image_list = ImageList(self, current_image_path=self.current_image_path, image_display=self.image_display)
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

    def print_focused_widget(self, event=None):
        focused_widget = self.focus_get()
        if not focused_widget:
            print("No focused widget. Setting focus to Treeview.")
            self.image_list.tree.focus_set()
        else:
            print(f"Focused widget: {focused_widget}")

    def on_closing(self):
        self.image_grouping.save_config()
        self.destroy()

if __name__ == "__main__":
    app = ViewerWindow()
    app.mainloop()