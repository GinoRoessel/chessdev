from database.base import Base, create_tables,delete_tables, get_session
import tkinter as tk
from chesspieces import *
from chessrules import *
from chessmove import *
from chessgui import *
from chessboard import *
from chessgame import *

if __name__== "__main__":
    delete_tables()
    create_tables()
    session=get_session()
    root=tk.Tk()

    game=ChessGame(root,session)
    gui=ChessGUI(root,game)
    root.mainloop() 
     
    ###

# if __name__== "__main__":
#     delete_tables()
#     # create_tables()
#     # session=get_session()
#     # root=tk.Tk()

#     # game=ChessGame(root,session)
#     # gui=ChessGUI(root,game)
#     # root.mainloop() 
     
#     # ###