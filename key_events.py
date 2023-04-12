import tkinter as tk

class KeyEvents:
    def __init__(self, parent, image_display, image_list):
        self.parent = parent  # 親ウィジェットを保持
        self.image_display = image_display  # ImageDisplayオブジェクトを保持
        self.image_list = image_list  # ImageListオブジェクトを保持
        self.bind_key_events()  # キーバインドの設定
        
    def bind_key_events(self):
        # スペースキーが押されたときに、画像を開くダイアログを表示
        self.parent.bind("<space>", lambda e: self.parent.open_folder_dialog())
        
        # Escキーが押されたときに、アプリケーションを終了
        self.parent.bind("<Escape>", lambda e: self.parent.destroy())
        
        # 上矢印キーが押されたときに、前の画像を表示
        self.parent.bind("<Up>", lambda e: self.previous_image(e))
        
        # 下矢印キーが押されたときに、次の画像を表示
        self.parent.bind("<Down>", lambda e: self.next_image(e))