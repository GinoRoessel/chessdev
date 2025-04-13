import tkinter as tk
from chesspieces import *
from chessmove import *
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
        

    
    def on_square_click(self,r,c): #button command
        if self.chessboard_.status!="white is mated, game over" and self.chessboard_.status!="black is mated, game over":
            if self.chessboard_.selected_piece!=None:
                move_to_prove=ChessMove((self.chessboard_.selected_pos[0],self.chessboard_.selected_pos[1]),(r,c),
                                        self.chessboard_.selected_piece)
                self.chessboard_.current_move=self.checking_move(move_to_prove)
                if self.chessboard_.current_move:
                    self.chessboard_.make_move(self.chessboard_.current_move)
                    self.chessboard_.current_player="black" if self.chessboard_.current_player=="white" else "white"
                    self.checkthegame()
                    if self.update_gui_ :
                        self.update_gui_(self.chessboard_.current_player,self.chessboard_.status)
                    if self.changes_gui_:
                        move_=self.chessboard_.current_move
                        if move_.is_enpassant==False and move_.is_castle==False and move_.is_promotion==False:
                            self.changes_gui_(move_.startpos[0],move_.startpos[1],self.chessboard_.board[move_.startpos[0]][move_.startpos[1]])
                            self.changes_gui_(move_.endpos[0],move_.endpos[1],self.chessboard_.board[move_.endpos[0]][move_.endpos[1]])
                        elif move_.is_enpassant==True:
                            self.changes_gui_(move_.startpos[0],move_.startpos[1],self.chessboard_.board[move_.startpos[0]][move_.startpos[1]])
                            self.changes_gui_(move_.endpos[0],move_.endpos[1],self.chessboard_.board[move_.endpos[0]][move_.endpos[1]])
                            self.changes_gui_(move_.captured_piece.position[0],move_.captured_piece.position[1],self.chessboard_.board[move_.captured_piece.position[0]][move_.captured_piece.position[1]])
                        elif move_.is_castle==True:
                            self.changes_gui_(move_.startpos[0],move_.startpos[1],self.chessboard_.board[move_.startpos[0]][move_.startpos[1]])
                            self.changes_gui_(move_.endpos[0],move_.endpos[1],self.chessboard_.board[move_.endpos[0]][move_.endpos[1]])
                            self.changes_gui_(move_.castle_secondpiece_pos[0],move_.castle_secondpiece_pos[1],self.chessboard_.board[move_.castle_secondpiece_pos[0]][move_.castle_secondpiece_pos[1]])
                            self.changes_gui_(move_.startpos[0],(move_.startpos[1]+move_.endpos[1])//2,self.chessboard_.board[move_.startpos[0]][(move_.startpos[1]+move_.endpos[1])//2])
                        elif move_.is_promotion==True:
                            self.changes_gui_(move_.startpos[0],move_.startpos[1],self.chessboard_.board[move_.startpos[0]][move_.startpos[1]])
                            self.changes_gui_(move_.endpos[0],move_.endpos[1],self.chessboard_.board[move_.endpos[0]][move_.endpos[1]])

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
    
    def checking_move(self,move__): 
        return Rules.is_valid_move(move__,self.chessboard_,self.promotion_choice_)

            
    def checkthegame(self): #check or mate?
        if Rules.checking_check(self.chessboard_.current_player,self.chessboard_):
            if Rules.checking_mate(self.chessboard_.current_player,self.chessboard_):
                self.chessboard_.status=f"{self.chessboard_.current_player} is mated, game over"
            else :
                self.chessboard_.status=f"{self.chessboard_.current_player} is in check"         
        else:
            self.chessboard_.status=" "

    def restartgame(self):
        self.chessboard_.setup_board(self.chessboard_.ruleset_) 
        self.chessboard_.selected_piece=None
        self.chessboard_.selected_pos=None
        self.chessboard_.current_player="white"
        self.chessboard_.status=" "
        if self.setup_gui_:
            self.setup_gui_(self.chessboard_.ruleset_,self.chessboard_.status,self.chessboard_.current_player)

        
        

