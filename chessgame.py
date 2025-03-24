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
        self.selected_piece=None
        self.selected_pos=None
        self.current_player="white"
        self.status=" "
        self.chessgui=ChessGUI(root,self) 
        self.chessgui.setup_gui(self.ruleset_,self.status,self.current_player)
        self.current_move=None

    
    def on_square_click(self,r,c): #button command
        if self.status!="white is mated, game over" and self.status!="black is mated, game over":
            if self.selected_piece!=None:
                if self.checking_move(self.selected_piece,
                                    self.selected_pos[0],self.selected_pos[1],r,c):
                    self.make_move(self.selected_piece,self.selected_pos[0],self.selected_pos[1],r,c)
                    self.current_player="black" if self.current_player=="white" else "white"
                    self.checkthegame()
                    self.chessgui.gui_update(self.current_player,self.status)
                    for m in self.current_move:
                        if m[1]!=None or m[2]!=None:
                            self.chessgui.gui_changes(m[1],m[2],self.chessboard_.board[m[1]][m[2]])
                        if m[3]!=None or m[4]!=None:
                            self.chessgui.gui_changes(m[3],m[4],self.chessboard_.board[m[3]][m[4]])
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

    def make_move(self,piece,startrow,startcol,endrow,endcol): #updating the data structures for a complete move
        #for example the castle has 2 single moves
        self.current_move=Rules.extract_moves_from_informations(piece,startrow,startcol,endrow,endcol,self.ruleset_,self.chessboard_)
        for move in self.current_move:
            self.make_single_move(move[0],move[1],move[2],move[3],move[4])

    def make_single_move(self,piece,startrow,startcol,endrow,endcol): #updating the data structures for a single move
        if endrow!=None and endcol!=None and startrow!=None and startcol!=None: #normal move
            self.chessboard_.deleting_piece((endrow,endcol))
            self.chessboard_.board[endrow][endcol]=piece
            self.chessboard_.board[endrow][endcol].position=(endrow,endcol)
        if endrow==None and endcol==None and startrow!=None and startcol!=None: #delete a piece
            self.chessboard_.deleting_piece((startrow,startcol))
        if startrow==None and startcol==None and endcol!=None and endrow!=None: #spawn new piece
            self.chessboard_.board[endrow][endcol]=piece
            self.chessboard_.board[endrow][endcol].position=(endrow,endcol)
            self.chessboard_.piece_lookup[self.chessboard_.board[endrow][endcol].symbol,self.chessboard_.board[endrow][endcol].color].append(self.chessboard_.board[endrow][endcol])
            if piece.color=="white":
                self.chessboard_.whitepieces.append(self.chessboard_.board[endrow][endcol])
            else:
                self.chessboard_.blackpieces.append(self.chessboard_.board[endrow][endcol])
        if startrow!=None and startcol!=None: #always except new thing spawned
            self.chessboard_.board[startrow][startcol]=None
            
    def checkthegame(self): #check or mate?
        if Rules.checking_check(self.chessboard_,self.current_player,self.ruleset_):
            if Rules.checking_mate(self.chessboard_,self.current_player,self.ruleset_):
                self.status=f"{self.current_player} is mated, game over"
            else :
                self.status=f"{self.current_player} is in check"         
        else:
            self.status=" "

    def restartgame(self):
        self.chessboard_.setup_board(self.ruleset_,self) 
        self.selected_piece=None
        self.selected_pos=None
        self.current_player="white"
        self.status=" "
        self.chessgui.setup_gui(self.ruleset_,self.status,self.current_player)

        
        

