from tkinter import *

def click():
    print("Hello World")

win = Tk()
win.geometry("800x1000")

btn = Button()
btn.config(command = click)
btn.pack()

mainloop()