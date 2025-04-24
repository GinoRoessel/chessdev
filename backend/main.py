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
    new_move = ChessMove(6,0,4,0,Pawn("white"))
    session.add(new_move)
    session.commit() 
    a= session.query(ChessMove).filter_by(startposx=0).first()
    print("yea",a.piece)
    
    game=ChessGame(root,session)
    gui=ChessGUI(root,game)
    root.mainloop() 
     
    ###