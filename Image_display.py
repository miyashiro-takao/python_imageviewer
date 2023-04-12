import tkinter as tk
from PIL import Image, ImageTk
import os

class ImageDisplay(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent)

        self.current_image = None
        self.photo = None
        self.bind("<Configure>", self.show_image)

        self.zoom = "fit"

        self.label = tk.Label(self)
        self.label.pack(fill=tk.BOTH, expand=True)

    # 画像を読み込む関数
    def load_image(self, image_path):
        self.current_image = Image.open(image_path)
        self.show_image()

    # 画像を表示する関数
    def show_image(self, event=None):
        if self.current_image is None:  # 現在の画像がない場合は処理を中断
            return

        if self.zoom == "fit":  # ズームが "fit" の場合
            img_width, img_height = self.current_image.size  # 画像のサイズを取得

            # ウィンドウに合わせる
            width_ratio = self.winfo_width() / img_width  # 横方向のリサイズ比率を計算
            height_ratio = self.winfo_height() / img_height  # 縦方向のリサイズ比率を計算
            resize_ratio = min(width_ratio, height_ratio)  # 小さい方のリサイズ比率を採用
            img_width = int(img_width * resize_ratio)  # リサイズ後の横サイズを計算
            img_height = int(img_height * resize_ratio)  # リサイズ後の縦サイズを計算

            # 画像サイズ変更
            self.current_image = self.current_image.resize((img_width, img_height), Image.ANTIALIAS)  # 画像をリサイズ
        elif self.zoom == "original":  # ズームが "original" の場合
            # 画像のオリジナルサイズを使用
            pass

        self.photo = ImageTk.PhotoImage(self.current_image)  # PhotoImageオブジェクトを作成

        # 画像を表示するためのラベル
        self.label.config(image=self.photo)  # ラベルにPhotoImageオブジェクトを設定
        self.label.image = self.photo  # ラベルに画像を保持させるための設定


    # ウィンドウに合わせて画像を表示する関数
    def fit_to_window(self):
        self.zoom = "fit"
        self.show_image()

    # 画像をオリジナルサイズで表示する関数
    def original_size(self):
        self.zoom = "original"
        self.show_image()
