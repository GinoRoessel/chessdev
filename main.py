import tkinter as tk
from chesspieces import *
from chessrules import *
from chessgui import *
from chessboard import *
from chessgame import *

if __name__== "__main__":
    root=tk.Tk()
    game=ChessGame(root)
    root.mainloop()