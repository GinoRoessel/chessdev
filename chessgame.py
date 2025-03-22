import tkinter as tk
from chesspieces import *
from chessrules import *
from chessgui import *
from chessboard import *

class ChessGame:
    def __init__(self,root):
        self.ruleset_="classical"
        self.chessboard_=ChessBoard() #all data structures
        self.chessboard_.setup_board(self.ruleset_,self)
        self.chessgui=ChessGUI(root,self) 
        self.chessgui.setup_gui(self.ruleset_)
        self.selected_piece=None
        self.selected_pos=None
        self.current_player="white"
        self.status=" "

    
    def on_square_click(self,r,c): #button command
        if self.status!="white is mated, game over" and self.status!="black is mated, game over":
            if self.selected_piece!=None:
                if self.checking_move(self.selected_piece,
                                    self.selected_pos[0],self.selected_pos[1],r,c):
                    self.make_move(self.selected_piece,self.selected_pos[0],self.selected_pos[1],r,c)
                    self.current_player="black" if self.current_player=="white" else "white"
                    self.checkthegame()
                    self.chessgui.gui_update(self.selected_pos[0],self.selected_pos[1],r,c,self.chessboard_,self.current_player,self.status)
                self.selected_piece=None
                self.selected_pos=None
                # print(self.selected_pos)
                # print(self.selected_piece)
            else:
                piece=self.chessboard_.board[r][c]
                if piece and piece.color==self.current_player: 
                    self.selected_piece=self.chessboard_.board[r][c]
                    self.selected_pos=(r,c)
                    # print(self.selected_pos)
                    # print(self.selected_piece)
    
    def checking_move(self,piece,startrow,startcol,endrow,endcol): 
        return Rules.is_valid_move(piece,startrow,startcol,endrow,endcol,self.ruleset_,self.chessboard_)

    def make_move(self,piece,startrow,startcol,endrow,endcol): #updating the data structures
        print("gelöscht wird",self.chessboard_.board[endrow][endcol])
        self.chessboard_.deleting_piece((endrow,endcol))
        print(len(self.chessboard_.blackpieces))
        self.chessboard_.board[endrow][endcol]=piece
        self.chessboard_.board[startrow][startcol]=None
        self.chessboard_.board[endrow][endcol].position=(endrow,endcol)

    def checkthegame(self): #check or mate?
        if Rules.checking_check(self.chessboard_,self.current_player,self.ruleset_):
            if Rules.checking_mate(self.chessboard_,self.current_player,self.ruleset_):
                self.status=f"{self.current_player} is mated, game over"
            else :
                self.status=f"{self.current_player} is in check"         
        else:
            self.status=" "

        
        

