# -*- coding: utf-8 -*-
from ttk import Frame, Button, Style
from Tkinter import Tk
import tkMessageBox as Box
from pygs import App
"""
Nie wiem, słabo to wygląda i nie ogarniam :v
@WJ
"""



class Menu(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent        
        self.initUI()
        
    def initUI(self):
      
        self.parent.title("Roguelike Game")
        self.style = Style()
        self.style.theme_use("default")
        self.pack()
        
        play_button = Button(self, text="Play Game", command=self.onPlay, width=25)
        play_button.grid()
        info_button = Button(self, text="Info", command=self.onInfo, width=25)
        info_button.grid(row=1, column=0)

    def onPlay(self):
        __TheApp__ = App()
        __TheApp__.execute()

    def onInfo(self):
        Box.showinfo("Information", "Taka giera na programowanie w pytongu ~Szymen, Wiktur & Tomek")


def build_gui():
  
    root = Tk()
    _ = Menu(root)
    root.geometry("250x100+100+100")
    Button(root, text="Exit", command=root.quit, width=25).pack()
    root.mainloop()

if __name__ == '__main__':
    build_gui()