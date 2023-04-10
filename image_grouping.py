import os
import shutil
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog

class ImageGrouping(tk.Frame):
    ICON_SIZE = (64, 64)
    LABEL_PADDING = {'padx': 5, 'pady': 0}

    def __init__(self, master=None):
        super().__init__(master)

        self.setup_ui()

    def setup_ui(self):
        # アイコン画像を読み込み、サイズ変更
        img = Image.open("icon.png")
        img = img.resize((64, 64), Image.ANTIALIAS)
        img_tk = ImageTk.PhotoImage(img)

        # 各フォルダ名を格納するための StringVar のリストを作成
        folder_name_vars = [tk.StringVar() for _ in range(4)]

        # フォルダアイコンとフォルダ名ラベルを作成
        for i in range(4):
            # フォルダアイコンを表示するラベルを作成
            label = tk.Label(self, image=img_tk)
            label.image = img_tk
            label.grid(row=0, column=i, **self.LABEL_PADDING)
            # フォルダアイコンがクリックされたときのイベントを設定
            label.bind("<Button-1>", lambda event, idx=i: self.open_folder_dialog(folder_name_vars[idx], idx))

            # フォルダ名を表示するラベルを作成
            folder_name_label = tk.Label(self, textvariable=folder_name_vars[i])
            folder_name_label.grid(row=1, column=i, **self.LABEL_PADDING)

        # 画像を表示するためのラベルを作成
        image_label = tk.Label(self)
        image_label.grid(row=2, column=0, columnspan=4, padx=5, pady=10)

        # 現在の画像のパスを保持するためのリストを作成
        current_image_path = [""]

        # キーバインディングを設定して、指定されたキーが押されたときに move_image 関数が呼び出されるようにします。
        self.bind('z', lambda event: self.move_image(current_image_path, folder_name_vars, 0))
        self.bind('Z', lambda event: self.move_image(current_image_path, folder_name_vars, 0))
        self.bind('x', lambda event: self.move_image(current_image_path, folder_name_vars, 1))
        self.bind('X', lambda event: self.move_image(current_image_path, folder_name_vars, 1))
        self.bind('c', lambda event: self.move_image(current_image_path, folder_name_vars, 2))
        self.bind('C', lambda event: self.move_image(current_image_path, folder_name_vars, 2))
        self.bind('v', lambda event: self.move_image(current_image_path, folder_name_vars, 3))
        self.bind('V', lambda event: self.move_image(current_image_path, folder_name_vars, 3))

    # 選択されたフォルダに画像を移動する関数
    def move_image(self, current_image_path, folder_name_vars, index):
        if current_image_path[0] and folder_name_vars[index].get():
            dest_folder = folder_name_vars[index].get()
            dest_path = os.path.join(dest_folder, os.path.basename(current_image_path[0]))
            shutil.move(current_image_path[0], dest_path)
            print(f"画像を移動しました: {current_image_path[0]} -> {dest_path}")
            current_image_path[0] = ""

    # フォルダ選択ダイアログを開く関数
    def open_folder_dialog(self, folder_name_var, index):
        selected_folder = filedialog.askdirectory()
        if selected_folder:
            folder_name = os.path.basename(selected_folder)
            folder_name_var.set(folder_name)
            print(f"選択されたフォルダ (インデックス {index}):", selected_folder)

def main():
    app = ImageGrouping()
    app.mainloop()

if __name__ == "__main__":
    main()
