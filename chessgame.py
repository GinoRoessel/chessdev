import tkinter as tk
from chesspieces import *
from chessrules import *
from chessboard import *

class ChessGame:
    def __init__(self,root):
        self.chessboard_=ChessBoard() #all data structures
        self.chessboard_.setup_board(self)
        #gui functions
        self.setup_gui_=None
        self.update_gui_=None
        self.changes_gui_=None
        self.promotion_choice_=None
        # self.chessgui.promotion_choice(self.chessboard_.current_player)

    
    def on_square_click(self,r,c): #button command
        if self.chessboard_.status!="white is mated, game over" and self.chessboard_.status!="black is mated, game over":
            if self.chessboard_.selected_piece!=None:
                if self.checking_move(self.chessboard_.selected_piece,
                                    self.chessboard_.selected_pos[0],self.chessboard_.selected_pos[1],r,c):
                    self.make_move(self.chessboard_.selected_piece,self.chessboard_.selected_pos[0],self.chessboard_.selected_pos[1],r,c)
                    self.chessboard_.move_list.append((self.chessboard_.selected_piece,(r,c)))
                    self.chessboard_.current_player="black" if self.chessboard_.current_player=="white" else "white"
                    self.checkthegame()
                    if self.update_gui_ :
                        self.update_gui_(self.chessboard_.current_player,self.chessboard_.status)
                    if self.changes_gui_:
                        for m in self.chessboard_.current_move:
                            if m[1]!=None or m[2]!=None:
                                self.changes_gui_(m[1],m[2],self.chessboard_.board[m[1]][m[2]])
                            if m[3]!=None or m[4]!=None:
                                self.changes_gui_(m[3],m[4],self.chessboard_.board[m[3]][m[4]])
                self.chessboard_.selected_piece=None
                self.chessboard_.selected_pos=None
                # print(self.chessboard_.selected_pos)
                # print(self.chessboard_.selected_piece)
            else:
                piece=self.chessboard_.board[r][c]
                if piece and piece.color==self.chessboard_.current_player: 
                    self.chessboard_.selected_piece=self.chessboard_.board[r][c]
                    self.chessboard_.selected_pos=(r,c)
                    # print(self.chessboard_.selected_pos)
                    # print(self.chessboard_.selected_piece)
    
    def checking_move(self,piece,startrow,startcol,endrow,endcol): 
        return Rules.is_valid_move(piece,startrow,startcol,endrow,endcol,self.chessboard_.ruleset_,self.chessboard_,self.chessboard_.move_list)

    def make_move(self,piece,startrow,startcol,endrow,endcol): #updating the data structures for a complete move
        #for example the castle has 2 single moves
        self.chessboard_.current_move=Rules.extract_moves_from_informations(piece,startrow,startcol,endrow,endcol,self.chessboard_.ruleset_,self.chessboard_,self.promotion_choice_)
        for move in self.chessboard_.current_move:
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
        if Rules.checking_check(self.chessboard_,self.chessboard_.current_player,self.chessboard_.ruleset_,self.chessboard_.move_list):
            if Rules.checking_mate(self.chessboard_,self.chessboard_.current_player,self.chessboard_.ruleset_,self.chessboard_.move_list):
                self.chessboard_.status=f"{self.chessboard_.current_player} is mated, game over"
            else :
                self.chessboard_.status=f"{self.chessboard_.current_player} is in check"         
        else:
            self.chessboard_.status=" "

    def restartgame(self):
        self.chessboard_.setup_board(self.chessboard_.ruleset_,self) 
        self.chessboard_.selected_piece=None
        self.chessboard_.selected_pos=None
        self.chessboard_.current_player="white"
        self.chessboard_.status=" "
        if self.setup_gui_:
            self.setup_gui_(self.chessboard_.ruleset_,self.chessboard_.status,self.chessboard_.current_player)

        
        

