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
        if self.current_image is None:
            return

        if self.zoom == "fit":
            img_width, img_height = self.current_image.size

            # ウィンドウに合わせる
            width_ratio = self.winfo_width() / img_width
            height_ratio = self.winfo_height() / img_height
            resize_ratio = min(width_ratio, height_ratio)
            img_width = int(img_width * resize_ratio)
            img_height = int(img_height * resize_ratio)

            # 画像サイズ変更
            self.current_image = self.current_image.resize((img_width, img_height), Image.ANTIALIAS)
        elif self.zoom == "original":
            # 画像のオリジナルサイズ
            pass

        self.photo = ImageTk.PhotoImage(self.current_image)

        # 画像を表示するためのラベル
        self.label.config(image=self.photo)
        self.label.image = self.photo

    # ウィンドウに合わせて画像を表示する関数
    def fit_to_window(self):
        self.zoom = "fit"
        self.show_image()

    # 画像をオリジナルサイズで表示する関数
    def original_size(self):
        self.zoom = "original"
        self.show_image()
