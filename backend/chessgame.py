
import tkinter as tk
from chesspieces import *
from chessmove import *
from chessrules import *
from chessboard import *
from chessgamedata import *
from sqlalchemy import select
from database.base import Base, create_tables,delete_tables, get_session
import copy

class ChessGame:
    def __init__(self,root,session):
        self.session=session
        self.chessgamedata=ChessGameData()
        self.session.add(self.chessgamedata)
        self.session.commit()
        self.chessboard_=ChessBoard(self.chessgamedata.id) #all data structures
        self.chessboard_.setup_board(self,self.chessgamedata.ruleset_)
        self.session.add(self.chessboard_)
        self.session.commit()
        #gui functions
        self.setup_gui_=None
        self.synchro_gui_=None
        self.update_gui_=None
        self.changes_gui_=None
        self.promotion_choice_=None
        #

    
    def on_square_click(self,r,c): #button command for the squares
        print("touched")
        if self.chessgamedata.status!="white is mated, game over" and self.chessgamedata.status!="black is mated, game over":
            if self.chessgamedata.selected_piece!=None: #if you selected a piece
                move_to_prove=ChessMove(self.chessboard_.id,self.chessgamedata.selected_posy,self.chessgamedata.selected_posx,r,c,
                                        self.chessgamedata.selected_piece)
                self.chessboard_.current_move=self.checking_move(move_to_prove)
                if self.chessboard_.current_move:
                    self.chessboard_.make_move(self.session,self.chessboard_.current_move)
                    cmove=self.chessboard_.current_move
                    print("made a move")
                    self.session.add(cmove)
                    self.session.commit()
                    self.chessboard_.current_move=cmove
                    print("PPPPP",self.chessboard_.current_move.id)
                    # print("beforecheck",self.chessboard_.board[1][5])
                    self.chessgamedata.current_player="black" if self.chessgamedata.current_player=="white" else "white"
                    self.checkthegame()
                    self.session.commit()
                    if self.chessgamedata.chessgame_ended==True:
                        self.replay_game_mode()
                    self.session.commit()
                    # print("aftercheck",self.chessboard_.board[1][5])
                    if self.update_gui_ :
                        self.update_gui_(self.chessgamedata.current_player,self.chessgamedata.status)
                    if self.changes_gui_:
                        move_=self.chessboard_.current_move
                        if move_.is_enpassant==False and move_.is_castle==False and move_.is_promotion==False:
                            # print("startpos",move_.startposy,move_.startposx)
                            # print("endpos",move_.endposy,move_.endposx)
                            self.changes_gui_(move_.startposy,move_.startposx,self.chessboard_.board[move_.startposy][move_.startposx])
                            self.changes_gui_(move_.endposy,move_.endposx,self.chessboard_.board[move_.endposy][move_.endposx])
                        elif move_.is_enpassant==True:
                            self.changes_gui_(move_.startposy,move_.startposx,self.chessboard_.board[move_.startposy][move_.startposx])
                            self.changes_gui_(move_.endposy,move_.endposx,self.chessboard_.board[move_.endposy][move_.endposx])
                            self.changes_gui_(move_.captured_piece.positiony,move_.captured_piece.positionx,self.chessboard_.board[move_.captured_piece_posy][move_.captured_piece_posx])
                        elif move_.is_castle==True:
                            self.changes_gui_(move_.startposy,move_.startposx,self.chessboard_.board[move_.startposy][move_.startposx])
                            self.changes_gui_(move_.endposy,move_.endposx,self.chessboard_.board[move_.endposy][move_.endposx])
                            self.changes_gui_(move_.castle_secondpiece_posy,move_.castle_secondpiece_posx,self.chessboard_.board[move_.castle_secondpiece_posy][move_.castle_secondpiece_posx])
                            self.changes_gui_(move_.startposy,(move_.startposx+move_.endposx)//2,self.chessboard_.board[move_.startposy][(move_.startposx+move_.endposx)//2])
                        elif move_.is_promotion==True:
                            self.changes_gui_(move_.startposy,move_.startposx,self.chessboard_.board[move_.startposy][move_.startposx])
                            self.changes_gui_(move_.endposy,move_.endposx,self.chessboard_.board[move_.endposy][move_.endposx])

                self.chessgamedata.selected_piece=None
                self.chessgamedata.selected_posy=None
                self.chessgamedata.selected_posx=None
                # print(self.chessboard_.selected_pos)
                # print(self.chessboard_.selected_piece)
            else: #now selecting a piece
                # print("select piece check")
                piece=self.chessboard_.board[r][c]
                # print(piece)
                # print(self.chessboard_.piece_lookup["Q","white"])
                if piece and piece.color==self.chessgamedata.current_player: 
                    # print("valid selelct piece")
                    self.chessgamedata.selected_piece=self.chessboard_.board[r][c]
                    self.chessgamedata.selected_posy=r
                    self.chessgamedata.selected_posx=c
                    # print(self.chessboard_.selected_pos)
                    # print(self.chessboard_.selected_piece)
    
    def checking_move(self,move__): #is the move legal?
        return Rules.is_valid_move(self.session,move__,self.chessgamedata,self.chessboard_,self.promotion_choice_)
        

            
    def checkthegame(self): #check or mate?
        if Rules.checking_check(self.session,self.chessgamedata.current_player,self.chessgamedata,self.chessboard_):
            if Rules.checking_mate(self.session,self.chessgamedata.current_player,self.chessgamedata,self.chessboard_):
                self.chessgamedata.status=f"{self.chessgamedata.current_player} is mated, game over"
                self.chessgamedata.chessgame_ended=True
            else :
                self.chessgamedata.status=f"{self.chessgamedata.current_player} is in check"         
        else:
            self.chessgamedata.status=" "

    def restartgame(self): #new game
        new_gamedata=ChessGameData()
        self.chessgamedata=new_gamedata
        self.session.add(self.chessgamedata)
        self.session.commit()
        new_board=ChessBoard(new_gamedata.id)
        self.chessboard_=new_board
        self.chessboard_.setup_board(self,self.chessgamedata.ruleset_) 
        # self.chessgamedata.selected_piece=None
        # self.chessgamedata.selected_posy=None
        # self.chessgamedata.selected_posx=None
        # self.chessgamedata.current_player="white"
        # self.chessgamedata.status=" "
        # self.chessboard_.move_list=[]
        self.session.add(self.chessboard_)
        self.session.commit()
        if self.synchro_gui_:
            self.synchro_gui_(self.chessboard_.board,self.chessgamedata.status,self.chessgamedata.current_player)

    def nextgame(self):
        new_next=self.get_nextgame()
        if new_next[0] and new_next[1]:
            self.chessgamedata=new_next[0]
            self.chessboard_=new_next[1]
            if self.synchro_gui_:
                self.synchro_gui_(self.chessboard_.board,self.chessgamedata.status,self.chessgamedata.current_player)
        else:
            print("no next game")

    def get_nextgame(self):
        new_next_gamedata=self.get_next_game_gamedata()
        if new_next_gamedata:
            new_next_board=self.get_last_game_board(new_next_gamedata.id)
            return new_next_gamedata,new_next_board
        else:
            return None,None

    def get_next_game_gamedata(self):
        return self.session.execute(
            select(ChessGameData)
            .where(ChessGameData.id > self.chessgamedata.id)
            .order_by(ChessGameData.id.asc())
            .limit(1)
        ).scalar_one_or_none()
    
    def get_next_game_board(self, gamedata_id_):
        return self.session.execute(
            select(ChessBoard).where(ChessBoard.gamedata_id== gamedata_id_)
        ).scalar_one_or_none()

    def lastgame(self):
        new_old=self.get_lastgame()
        if new_old[0] and new_old[1]:
            self.chessgamedata=new_old[0]
            self.chessboard_=new_old[1]
            if self.synchro_gui_:
                self.synchro_gui_(self.chessboard_.board,self.chessgamedata.status,self.chessgamedata.current_player)
        else: 
            print("no last game")

    def get_lastgame(self):
        new_old_gamedata=self.get_last_game_gamedata()
        if new_old_gamedata:
            new_old_board=self.get_last_game_board(new_old_gamedata.id)
            return new_old_gamedata,new_old_board
        else: 
            return None,None


    def get_last_game_gamedata(self):
        return self.session.execute(
            select(ChessGameData)
            .where(ChessGameData.id < self.chessgamedata.id)
            .order_by(ChessGameData.id.desc())
            .limit(1)
        ).scalar_one_or_none()
    
    def get_last_game_board(self, gamedata_id_):
        return self.session.execute(
            select(ChessBoard).where(ChessBoard.gamedata_id== gamedata_id_)
        ).scalar_one_or_none()

####
    def replay_game_mode(self):
        replay_board = ChessGame.deepcopy_board_without_id(self.chessboard_)
        print("YYYY",replay_board.gamedata_id, self.chessboard_.gamedata_id, replay_board.is_replay)
        self.session.add(replay_board)
        self.session.commit()

    @staticmethod
    def deepcopy_board_without_id(originalboard):
        dc=ChessBoard(originalboard.gamedata_id,is_replay=True)
        dc.whitepieces=copy.deepcopy(originalboard.whitepieces)
        dc.blackpieces=copy.deepcopy(originalboard.blackpieces)
        dc.piece_lookup=copy.deepcopy(originalboard.piece_lookup)
        dc.board=copy.deepcopy(originalboard.board)
        dc.current_move=copy.deepcopy(originalboard.current_move)
        return dc


    def lastmove(self):
        move_=self.get_last_move()
        print("ÖÖÖÖ")
        if move_:
            board=self.session.execute(
                                        select(ChessBoard)
                                        .where(ChessBoard.gamedata_id == self.chessboard_.gamedata_id,
                                            ChessBoard.is_replay==True)
                                        .order_by(ChessBoard.id.desc())
                                        .limit(1)
                                    ).scalar_one_or_none()
            print("ÜÜÜÜ")
            board.take_move_back(self.session,move_)
            if self.changes_gui_:
                    if move_.is_enpassant==False and move_.is_castle==False and move_.is_promotion==False:
                        # print("startpos",move_.startposy,move_.startposx)
                        # print("endpos",move_.endposy,move_.endposx)
                        self.changes_gui_(move_.startposy,move_.startposx,board.board[move_.startposy][move_.startposx])
                        self.changes_gui_(move_.endposy,move_.endposx,board.board[move_.endposy][move_.endposx])
                    elif move_.is_enpassant==True:
                        self.changes_gui_(move_.startposy,move_.startposx,board.board[move_.startposy][move_.startposx])
                        self.changes_gui_(move_.endposy,move_.endposx,board.board[move_.endposy][move_.endposx])
                        self.changes_gui_(move_.captured_piece.positiony,move_.captured_piece.positionx,board.board[move_.captured_piece_posy][move_.captured_piece_posx])
                    elif move_.is_castle==True:
                        self.changes_gui_(move_.startposy,move_.startposx,board.board[move_.startposy][move_.startposx])
                        self.changes_gui_(move_.endposy,move_.endposx,board.board[move_.endposy][move_.endposx])
                        self.changes_gui_(move_.castle_secondpiece_posy,move_.castle_secondpiece_posx,board.board[move_.castle_secondpiece_posy][move_.castle_secondpiece_posx])
                        self.changes_gui_(move_.startposy,(move_.startposx+move_.endposx)//2,board.board[move_.startposy][(move_.startposx+move_.endposx)//2])
                    elif move_.is_promotion==True:
                        self.changes_gui_(move_.startposy,move_.startposx,board.board[move_.startposy][move_.startposx])
                        self.changes_gui_(move_.endposy,move_.endposx,board.board[move_.endposy][move_.endposx])
            board.current_move=self.session.execute(
                                        select(ChessMove)
                                        .where(ChessMove.board_id == self.chessboard_.id,
                                            ChessMove.id<board.current_move.id)
                                        .order_by(ChessMove.id.desc())
                                        .limit(1)
                                    ).scalar_one_or_none()

    def get_last_move(self):
        board=self.session.execute(
                                        select(ChessBoard)
                                        .where(ChessBoard.gamedata_id == self.chessboard_.gamedata_id,
                                            ChessBoard.is_replay==True)
                                        .order_by(ChessBoard.id.desc())
                                        .limit(1)
                                    ).scalar_one_or_none()
        print("QQQQ")
        return board.current_move
    

    def nextmove(self):
        move_=self.get_next_move()
        if move_:
            board=self.session.execute(
                                        select(ChessBoard)
                                        .where(ChessBoard.gamedata_id == self.chessboard_.gamedata_id,
                                            ChessBoard.is_replay==True)
                                        .order_by(ChessBoard.id.desc())
                                        .limit(1)
                                    ).scalar_one_or_none()
            board.make_move(self.session,move_)
            if self.changes_gui_:
                    if move_.is_enpassant==False and move_.is_castle==False and move_.is_promotion==False:
                        # print("startpos",move_.startposy,move_.startposx)
                        # print("endpos",move_.endposy,move_.endposx)
                        self.changes_gui_(move_.startposy,move_.startposx,board.board[move_.startposy][move_.startposx])
                        self.changes_gui_(move_.endposy,move_.endposx,board.board[move_.endposy][move_.endposx])
                    elif move_.is_enpassant==True:
                        self.changes_gui_(move_.startposy,move_.startposx,board.board[move_.startposy][move_.startposx])
                        self.changes_gui_(move_.endposy,move_.endposx,board.board[move_.endposy][move_.endposx])
                        self.changes_gui_(move_.captured_piece.positiony,move_.captured_piece.positionx,board.board[move_.captured_piece_posy][move_.captured_piece_posx])
                    elif move_.is_castle==True:
                        self.changes_gui_(move_.startposy,move_.startposx,board.board[move_.startposy][move_.startposx])
                        self.changes_gui_(move_.endposy,move_.endposx,board.board[move_.endposy][move_.endposx])
                        self.changes_gui_(move_.castle_secondpiece_posy,move_.castle_secondpiece_posx,board.board[move_.castle_secondpiece_posy][move_.castle_secondpiece_posx])
                        self.changes_gui_(move_.startposy,(move_.startposx+move_.endposx)//2,board.board[move_.startposy][(move_.startposx+move_.endposx)//2])
                    elif move_.is_promotion==True:
                        self.changes_gui_(move_.startposy,move_.startposx,board.board[move_.startposy][move_.startposx])
                        self.changes_gui_(move_.endposy,move_.endposx,board.board[move_.endposy][move_.endposx])
            board.current_move=move_

    def get_next_move(self):
        board=self.session.execute(
                                        select(ChessBoard)
                                        .where(ChessBoard.gamedata_id == self.chessboard_.gamedata_id,
                                            ChessBoard.is_replay==True)
                                        .order_by(ChessBoard.id.desc())
                                        .limit(1)
                                    ).scalar_one_or_none()
        if  board.current_move:
            return self.session.execute(
                                            select(ChessMove)
                                            .where(ChessMove.board_id == self.chessboard_.id,
                                                ChessMove.id>board.current_move.id)
                                            .order_by(ChessMove.id.asc())
                                            .limit(1)
                                        ).scalar_one_or_none()
        else:
            return self.session.execute(
                                            select(ChessMove)
                                            .where(ChessMove.board_id == self.chessboard_.id)
                                            .order_by(ChessMove.id.asc())
                                            .limit(1)
                                        ).scalar_one_or_none()

        

