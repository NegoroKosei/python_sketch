import tkinter as tk
from tkinter import colorchooser

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("お絵描きソフト")

        # --- 設定値 ---
        self.pen_color = "black"
        self.pen_size = 5
        self.eraser_on = False

        # --- ウィジェットの作成 ---
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # 色選択ボタン
        self.color_button = tk.Button(self.control_frame, text="色を選択", command=self.choose_color)
        self.color_button.pack(side=tk.LEFT, padx=5)

        # ペン/消しゴム切り替えボタン
        self.pen_eraser_button = tk.Button(self.control_frame, text="消しゴム", command=self.toggle_eraser)
        self.pen_eraser_button.pack(side=tk.LEFT, padx=5)

        # 太さ調整スライダー
        self.size_label = tk.Label(self.control_frame, text="太さ:")
        self.size_label.pack(side=tk.LEFT, padx=(10, 0))
        self.size_slider = tk.Scale(self.control_frame, from_=1, to=50, orient=tk.HORIZONTAL, command=self.change_pen_size)
        self.size_slider.set(self.pen_size)
        self.size_slider.pack(side=tk.LEFT)
        
        # 全消しボタン
        self.clear_button = tk.Button(self.control_frame, text="全消し", command=self.clear_canvas)
        self.clear_button.pack(side=tk.RIGHT, padx=5)


        # 描画用キャンバス
        self.canvas = tk.Canvas(self.root, bg="white", width=800, height=600)
        self.canvas.pack(expand=True, fill=tk.BOTH)

        # --- イベントのバインド ---
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.reset_drawing)
        
        self.old_x = None
        self.old_y = None

    def choose_color(self):
        """色選択ダイアログを開き、ペンの色を設定する"""
        color_code = colorchooser.askcolor(title="色を選択")
        if color_code:
            self.pen_color = color_code[1]
            self.eraser_on = False
            self.pen_eraser_button.config(text="消しゴム", relief=tk.RAISED)

    def toggle_eraser(self):
        """ペンと消しゴムを切り替える"""
        self.eraser_on = not self.eraser_on
        if self.eraser_on:
            self.pen_eraser_button.config(text="ペン", relief=tk.SUNKEN)
        else:
            self.pen_eraser_button.config(text="消しゴム", relief=tk.RAISED)

    def change_pen_size(self, size):
        """スライダーの値でペンの太さを変更する"""
        self.pen_size = int(size)

    def clear_canvas(self):
        """キャンバスの内容をすべて消去する"""
        self.canvas.delete("all")

    def draw(self, event):
        """マウスのドラッグに合わせて線を描画する"""
        if self.old_x and self.old_y:
            # 消しゴムモードかどうかで色を決定
            draw_color = "white" if self.eraser_on else self.pen_color
            
            self.canvas.create_line(
                self.old_x, self.old_y, event.x, event.y,
                width=self.pen_size,
                fill=draw_color,
                capstyle=tk.ROUND, # 線の先端を丸くする
                smooth=tk.TRUE     # 線を滑らかにする
            )
        self.old_x = event.x
        self.old_y = event.y

    def reset_drawing(self, event):
        """マウスのボタンが離されたときに座標をリセット"""
        self.old_x = None
        self.old_y = None

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()