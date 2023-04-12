import os
import shutil
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
import configparser

class ImageGrouping(tk.Frame):
    ICON_SIZE = (64, 64)
    LABEL_PADDING = {'padx': 5, 'pady': 0}
    SECTION_FOLDERS = "folders"

    def __init__(self, master=None):
        super().__init__(master)
        self.folder_name_vars = [tk.StringVar() for _ in range(4)] # 各フォルダ名を格納するための StringVar のリストを作成
        self.config = configparser.ConfigParser()
        self.load_config() # 設定ファイルを読み込み
        self.setup_ui()
    
    def setup_ui(self):
        # アイコン画像を読み込み、サイズ変更
        img = Image.open("icon.png")
        img = img.resize((64, 64), Image.ANTIALIAS)
        img_tk = ImageTk.PhotoImage(img)

        # フォルダアイコンとフォルダ名ラベルを作成
        for i in range(4):
            # フォルダアイコンを表示するラベルを作成
            label = tk.Label(self, image=img_tk)
            label.image = img_tk
            label.grid(row=0, column=i, **self.LABEL_PADDING)
            # フォルダアイコンがクリックされたときのイベントを設定
            label.bind("<Button-1>", lambda event, idx=i: self.open_folder_dialog(self.folder_name_vars[idx], idx))

            # フォルダ名を表示するラベルを作成
            folder_name_label = tk.Label(self, textvariable=self.folder_name_vars[i])
            folder_name_label.grid(row=1, column=i, **self.LABEL_PADDING)

        # 画像を表示するためのラベルを作成
        image_label = tk.Label(self)
        image_label.grid(row=2, column=0, columnspan=4, padx=5, pady=10)

        # 現在の画像のパスを保持するためのリストを作成
        current_image_path = [""]

        # キーバインディングを設定して、指定されたキーが押されたときに move_image 関数が呼び出されるようにします。
        self.bind_all('z', lambda event: self.move_image(current_image_path, self.folder_name_vars, 0))
        self.bind_all('Z', lambda event: self.move_image(current_image_path, self.folder_name_vars, 0))
        self.bind_all('x', lambda event: self.move_image(current_image_path, self.folder_name_vars, 1))
        self.bind_all('X', lambda event: self.move_image(current_image_path, self.folder_name_vars, 1))
        self.bind_all('c', lambda event: self.move_image(current_image_path, self.folder_name_vars, 2))
        self.bind_all('C', lambda event: self.move_image(current_image_path, self.folder_name_vars, 2))
        self.bind_all('v', lambda event: self.move_image(current_image_path, self.folder_name_vars, 3))
        self.bind_all('V', lambda event: self.move_image(current_image_path, self.folder_name_vars, 3))

    # 選択されたフォルダに画像を移動する関数
    def move_image(self, current_image_path, folder_name_vars, index):
        print(current_image_path[0])
        print(folder_name_vars[index].get())
        if current_image_path[0] and folder_name_vars[index].get():  # 現在の画像パスと選択されたフォルダが存在する場合
            dest_folder = folder_name_vars[index].get()  # 移動先のフォルダを取得
            dest_path = os.path.join(dest_folder, os.path.basename(current_image_path[0]))  # 移動先のパスを作成
            shutil.move(current_image_path[0], dest_path)  # 画像を移動先のパスに移動
            print(f"画像を移動しました: {current_image_path[0]} -> {dest_path}")  # 移動した画像の情報を表示
            current_image_path[0] = ""  # 現在の画像パスをリセット


    # フォルダ選択ダイアログを開く関数
    def open_folder_dialog(self, folder_name_var, index):
        selected_folder = filedialog.askdirectory()
        if selected_folder:
            folder_name = os.path.basename(selected_folder)
            folder_name_var.set(folder_name)
            print(f"選択されたフォルダ (インデックス {index}):", selected_folder)
            self.config.set("folders", f"folder{index}", selected_folder)  # フルパスを設定ファイルに保存
            self.save_config()

    # 設定ファイルにフォルダ情報を保存する関数
    def save_config(self):
        with open("config.ini", "w", encoding='utf-8') as configfile:
            self.config.write(configfile)

    def load_config(self):
        config_file = "config.ini"
        
        if not os.path.isfile(config_file):
            with open(config_file, "w", encoding='utf-8') as file:
                file.write(f"[{self.SECTION_FOLDERS}]\n")  # 変更
                for i in range(4):
                    file.write(f"folder{i} = \n")
        
        self.config.read(config_file, encoding='utf-8')
        if not self.config.has_section(self.SECTION_FOLDERS):  # 変更
            self.config.add_section(self.SECTION_FOLDERS)  # 変更

        for i in range(4):
            if not self.config.has_option(self.SECTION_FOLDERS, f"folder{i}"):  # 変更
                self.config.set(self.SECTION_FOLDERS, f"folder{i}", "")  # 変更
            folder_path = self.config.get(self.SECTION_FOLDERS, f"folder{i}")  # 変更
            folder_name = os.path.basename(folder_path)  # フォルダ名を取得
            self.folder_name_vars[i].set(folder_name)    # フォルダ名を StringVar に設定

def main():
    app = ImageGrouping()
    app.mainloop()

if __name__ == "__main__":
    main()
