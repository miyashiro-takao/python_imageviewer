"""画像を表示するキャンバス用ウィジェット。"""

import tkinter as tk
from PIL import Image, ImageTk


class ImageDisplay(tk.Canvas):
    """画像のリサイズと描画を担当するクラス。"""

    def __init__(self, parent):
        super().__init__(parent)

        self.original_image = None
        self.current_image = None
        self.photo = None
        self.zoom = "fit"

        self.bind("<Configure>", self.show_image)

        self.label = tk.Label(self)
        self.label.pack(fill=tk.BOTH, expand=True)

    def load_image(self, image_path):
        """画像を読み込み、表示用に準備する。"""
        with Image.open(image_path) as source_image:
            self.original_image = source_image.copy()
        self.current_image = self.original_image
        self.show_image()

    def show_image(self, event=None):
        """現在のズーム設定に合わせて画像を描画する。"""
        if self.original_image is None:
            return

        image_to_display = self.original_image

        if self.zoom == "fit":
            img_width, img_height = image_to_display.size
            canvas_width = max(self.winfo_width(), 1)
            canvas_height = max(self.winfo_height(), 1)
            width_ratio = canvas_width / img_width
            height_ratio = canvas_height / img_height
            resize_ratio = min(width_ratio, height_ratio)
            new_width = max(1, int(img_width * resize_ratio))
            new_height = max(1, int(img_height * resize_ratio))
            # Pillow 10 以降は LANCZOS が高品質リサンプルとして推奨される。
            image_to_display = image_to_display.resize((new_width, new_height), Image.LANCZOS)

        self.current_image = image_to_display
        self.photo = ImageTk.PhotoImage(self.current_image)
        self.label.config(image=self.photo)
        self.label.image = self.photo

    def fit_to_window(self):
        """表示領域に合わせて画像サイズを調整する。"""
        self.zoom = "fit"
        self.show_image()

    def original_size(self):
        """画像を元のサイズで表示する。"""
        self.zoom = "original"
        self.show_image()
