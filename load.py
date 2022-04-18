import sys
import tkinter as tk


root = tk.Tk()

# ウインドウのタイトルを定義する
root.title(u'タイトル')

# ここでウインドウサイズを定義する
root.geometry('1000x600')

# Buttonを設置してみる
Button1 = tk.Button(text=u'画像切り替え')
Button1.pack()

root.mainloop()