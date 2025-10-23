tkinterを使用した画像ビューア  
画像分類機能追加

## 環境構築

1. Python 3.10 以降を用意します。macOS / Windows では標準で Tkinter が利用できます。Linux の場合は `sudo apt-get install python3-tk` などで Tkinter を追加してください。
2. 仮想環境を作成して有効化します。
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS / Linux
   ```
3. 依存パッケージをインストールします。
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## アプリの起動

```bash
python main.py
```
