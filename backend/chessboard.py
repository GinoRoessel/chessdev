from database.base import Base
from sqlalchemy import Column, Integer, String, Boolean
from chesspieces import *
from chessmove import *
from collections import defaultdict
from itertools import chain


class _ChessBoard:
    def __init__(self):
        self.ruleset_="classical"
        self.create_board()
        self.piece_lookup=defaultdict(list) #to lookup position of certain pieces
        self.whitepieces=[] #to iterate to all the pieces left
        self.blackpieces=[]
        #
        self.selected_piece=None
        self.selected_posy=None
        self.selected_posx=None
        self.current_player="white"
        self.status=" "
        self.current_move=None
        self.move_list=[]
        #

    def create_board(self):
        self.board=[[None for _ in range(8)] for _ in range(8)] #main data structure
    
    def setup_board(self,game):
        self.board=[[None for _ in range(8)] for _ in range(8)]
        self.piece_lookup=defaultdict(list) #to lookup position of certain pieces
        self.whitepieces=[] #to iterate to all the pieces left
        self.blackpieces=[]
        if self.ruleset_=="classical":
            self.setup_board_classical(game)
    
    def setup_board_classical(self,game):
        whitepieces_=[Rook("white"),Knight("white"),Bishop("white"),Queen("white"),
                              King("white"),Bishop("white"),Knight("white"),Rook("white")]
        blackpieces_=[Rook("black"),Knight("black"),Bishop("black"),Queen("black"),
                              King("black"),Bishop("black"),Knight("black"),Rook("black")]
        for i in range(len(whitepieces_)):
            self.board[7][i]=whitepieces_[i]
            self.board[6][i]=Pawn("white")
            self.board[1][i]=Pawn("black")
            self.board[0][i]=blackpieces_[i]
            self.board[7][i].positiony=7 
            self.board[7][i].positionx=i 
            self.board[6][i].positiony=6
            self.board[6][i].positionx=i
            self.board[1][i].positiony=1
            self.board[1][i].positionx=i
            self.board[0][i].positiony=0
            self.board[0][i].positionx=i
            # print(self.board[0][i])
            # print(self.board[0][i].position)
            self.piece_lookup[self.board[7][i].symbol,"white"].append(self.board[7][i]) #adding to the lookup_dict
            self.piece_lookup[self.board[0][i].symbol,"black"].append(self.board[0][i])
            self.piece_lookup[self.board[6][i].symbol,"white"].append(self.board[6][i])
            self.piece_lookup[self.board[1][i].symbol,"black"].append(self.board[1][i])
            self.whitepieces.append(self.board[7][i]) #adding to the simple list
            self.whitepieces.append(self.board[6][i])
            self.blackpieces.append(self.board[0][i])
            self.blackpieces.append(self.board[1][i])
        
    def deleting_piece(self,posy,posx): #delete it from all three datastructures
        if self.board[posy][posx]==None:
            return
        key=(self.board[posy][posx].symbol,self.board[posy][posx].color)
        # print("key:",key)
        if key in self.piece_lookup:
            # print("key found")
            if isinstance(self.piece_lookup[key],list):
                # print("its a list")
                # print(self.piece_lookup[key])
                for piece_ in self.piece_lookup[key]:
                    # print(piece_.position)
                    if piece_.positiony==posy and piece_.positionx==posx:
                        if piece_.color=="white":
                            self.whitepieces.remove(piece_)
                        elif piece_.color=="black":
                            self.blackpieces.remove(piece_)
                            # print("how many blackpieces left:",len(self.blackpieces))
                        self.piece_lookup[key].remove(piece_)
                        self.board[posy][posx]==None
                        return  



    def make_move(self,move_): #updating the data structures for a complete move
        #for example the castle has 2 single moves
        # self.chessboard_.current_move=Rules.extract_moves_from_informations(piece,startrow,startcol,endrow,endcol,self.chessboard_.ruleset_,self.chessboard_,self.promotion_choice_)
        # for move in self.chessboard_.current_move:
        if move_.is_enpassant==False and move_.is_castle==False and move_.is_promotion==False:
            # print("normaler move")
            self.make_single_move(move_)
        elif move_.is_enpassant==True:
            self.make_single_move(move_)
            self.make_single_move(ChessMove(move_.captured_piece_posy,move_.captured_piece_posx,None,None,move_.captured_piece))
        elif move_.is_castle==True:
            self.make_single_move(move_)
            self.make_single_move(ChessMove(move_.castle_secondpiece_posy,move_.castle_secondpiece_posx,move_.startposy,(move_.startposx+move_.endposx)//2,move_.castle_secondpiece))
        elif move_.is_promotion==True:
            self.make_single_move(move_)
            p_move=ChessMove(move_.endposy,move_.endposx,None,None,move_.piece)
            self.make_single_move(p_move)
            # print("promo choice",move_.promotion_choice)
            self.make_single_move(ChessMove(None,None,move_.endposy,move_.endposx,move_.promotion_choice))
        self.move_list.append(move_)



    def make_single_move(self,move_): #updating the data structures for a single move
        if move_.endposy!=None and move_.endposx!=None and move_.startposy!=None and move_.startposx!=None: #normal move
            self.deleting_piece(move_.endposy,move_.endposx)
            self.board[move_.endposy][move_.endposx]=move_.piece
            self.board[move_.endposy][move_.endposx].positiony=move_.endposy
            self.board[move_.endposy][move_.endposx].positionx=move_.endposx
        if move_.endposy==None and move_.endposx==None and move_.startposy!=None and move_.startposx!=None: #delete a piece
            self.deleting_piece(move_.startposy,move_.startposx)
        if move_.startposy==None and move_.startposx==None and move_.endposx!=None and move_.endposy!=None: #spawn new piece
            self.board[move_.endposy][move_.endposx]=move_.piece
            self.board[move_.endposy][move_.endposx].positiony=move_.endposy
            self.board[move_.endposy][move_.endposx].positionx=move_.endposx
            self.piece_lookup[self.board[move_.endposy][move_.endposx].symbol,self.board[move_.endposy][move_.endposx].color].append(self.board[move_.endposy][move_.endposx])
            if move_.piece.color=="white":
                self.whitepieces.append(self.board[move_.endposy][move_.endposx])
            else:
                self.blackpieces.append(self.board[move_.endposy][move_.endposx])
        if move_.startposy!=None and move_.startposx!=None: #always except new thing spawned
            self.board[move_.startposy][move_.startposx]=None

    def take_move_back(self,move_):
        if move_.is_enpassant==False and move_.is_castle==False and move_.is_promotion==False:
            self.take_single_move_back(move_)
            # print("before recreation of captured piece")
            if move_.captured_piece!=None:
                # print("recreation of captured piece")
                self.take_single_move_back(ChessMove(move_.captured_piece_posy,move_.captured_piece_posx,None,None,move_.captured_piece))
        elif move_.is_enpassant==True:
            self.take_single_move_back(move_)
            self.take_single_move_back(ChessMove(move_.captured_piece_posy,move_.captured_piece_posx,None,None,move_.captured_piece))
        elif move_.is_castle==True:
            self.take_single_move_back(move_)
            self.take_single_move_back(ChessMove(move_.captured_piece_posy,move_.captured_piece_posx,move_.startposy,(move_.startposx+move_.endposx)//2,move_.castle_secondpiece))
        elif move_.is_promotion==True:
            self.make_single_move(ChessMove(None,None,move_.endposy,move_.endposx,move_.promotion_choice))
            p_move=ChessMove(move_.endposy,move_.endposx,None,None,move_.piece)
            self.take_single_move_back(p_move)
            self.take_single_move_back(move_)
            if move_.captured_piece!=None:
                self.take_single_move_back(ChessMove(move_.captured_piece_posy,move_.captured_piece_posx,None,None,move_.captured_piece))
        self.move_list.pop()
            

    def take_single_move_back(self,move_):
        if move_.endposy!=None and move_.endposx!=None and move_.startposy!=None and move_.startposx!=None: #normal move
            self.board[move_.startposy][move_.startposx]=move_.piece
            self.board[move_.startposy][move_.startposx].positiony=move_.startposy
            self.board[move_.startposy][move_.startposx].positionx=move_.startposx
            self.board[move_.endposy][move_.endposx]=None
        if move_.endposy==None and move_.endposx==None and move_.startposy!=None and move_.startposx!=None: #delete a piece
            self.create_piece(move_.startposy,move_.startposx,move_.piece)
            # print("takeback smth")
            # if move_.piece.symbol=="Q":
            #     print("takeback a queen")
        if move_.startposy==None and move_.startposx==None and move_.endposx!=None and move_.endposy!=None: #spawn new piece
            self.deleting_piece(move_.endposy,move_.endposx)
        if move_.endposy!=None and move_.endposx!=None: #always except new thing spawned
            self.board[move_.endposy][move_.endposx]=None

    def create_piece(self,posy,posx,piece):
        # print("something created")
        self.board[posy][posx]=piece
        self.board[posy][posx].positiony=posy
        self.board[posy][posx].positionx=posx
        self.piece_lookup[self.board[posy][posx].symbol,self.board[posy][posx].color].append(self.board[posy][posx])
        if piece.color=="white":
            self.whitepieces.append(self.board[posy][posx])
        else:
            self.blackpieces.append(self.board[posy][posx])

class ChessBoard(Base):
    __tablename__ = 'chess_boards'

    id = Column(Integer, primary_key=True)
    ruleset_=Column(String)
    board=Column(String) 
    piece_lookup=Column(String,nullable=True) 
    whitepieces=Column(String,nullable=True) 
    blackpieces=Column(String,nullable=True) 
    selected_piece=Column(String,nullable=True) 
    selected_posy=Column(Integer,nullable=True)
    selected_posx=Column(Integer,nullable=True)
    current_player=Column(String)
    status=Column(String,nullable=True)
    current_move=Column(String,nullable=True)
    move_list=Column(String,nullable=True) 

    def __init__(self,session):
        self.session=session
        self._current_move=None
        self._selected_piece=None
        self._move_list=None
        self._whitepieces=None
        self._blackpieces=None
        self._piece_lookup=None
        self._board=None

        self.ruleset_="classical"
        self.create_board()
        self.piece_lookup=defaultdict(list) #to lookup position of certain pieces
        self.whitepieces=[] #to iterate to all the pieces left
        self.blackpieces=[]
        #
        self.selected_piece=None
        self.selected_posy=None
        self.selected_posx=None
        self.current_player="white"
        self.status=" "
        self.current_move=None
        self.move_list=[]
        #
    

    @property
    def board(self):
        if self._board:
            list_strings=json.loads(self._board)
            return [[ChessPieces.from_dict(p) for p in listy] for listy in list_strings]
        else:
            return []
    
    @board.setter
    def board(self, liste):
        if liste:
            self._board=json.dumps([[p.to_dict() if p is not None else None for p in listy ] for listy in liste])
        else:
            self._board=json.dumps([])

    @property
    def piece_lookup(self):
        if self._piece_lookup:
            dict_strings=json.loads(self._piece_lookup)
            dict__= {
                    key: [ChessPieces.from_dict(p) for p in value] for key, value in dict_strings.items()
            }
            return defaultdict(list, dict__)
        else:
            return defaultdict(list)
    
    @piece_lookup.setter
    def piece_lookup(self, dict_):
        if dict_:
            self._piece_lookup=json.dumps({key: [p.to_dict() for p in value] for key,value in dict_.items()})
        else:
            self._piece_lookup=json.dumps(dict())

    @property
    def whitepieces(self):
        if self._whitepieces:
            list_strings=json.loads(self._whitepieces)
            return [ChessPieces.from_dict(p) for p in list_strings]
        else:
            return []
    
    @whitepieces.setter
    def whitepieces(self, liste):
        if liste:
            self._whitepieces=json.dumps([p.to_dict() for p in liste])
        else:
            self._whitepieces=json.dumps([])

    @property
    def blackpieces(self):
        if self._blackpieces:
            list_strings=json.loads(self._blackpieces)
            return [ChessPieces.from_dict(p) for p in list_strings]
        else:
            return []
    
    @blackpieces.setter
    def blackpieces(self, liste):
        if liste:
            self._blackpieces=json.dumps([p.to_dict() for p in liste])
        else:
            self._blackpieces=json.dumps([])

    @property
    def selected_piece(self):
        if self._selected_piece:
            return ChessPieces.from_json(self._selected_piece)
        else:
            return None
    
    @selected_piece.setter
    def selected_piece(self, selected_piece_):
        if selected_piece_:
            self._selected_piece=selected_piece_.to_json()
        else:
            self._selected_piece=None

    @property
    def current_move(self):
        if self._current_move:
            return ChessMove.from_json(self._current_move)
        else:
            return None
    
    @current_move.setter
    def current_move(self, c_move):
        if c_move:
            self._current_move=c_move.to_json()
        else:
            self._current_move=None

    @property
    def move_list(self):
        if self._move_list:
            list_strings=json.loads(self._move_list)
            return [ChessMove.from_dict(mv) for mv in list_strings]
        else:
            return []
    
    @move_list.setter
    def move_list(self, liste):
        if liste:
            self._move_list=json.dumps([mv.to_dict() for mv in liste])
        else:
            self._move_list=json.dumps([])

    def create_board(self):
        self.board=[[None for _ in range(8)] for _ in range(8)] #main data structure
    
    def setup_board(self,game):
        self.board=[[None for _ in range(8)] for _ in range(8)]
        self.piece_lookup=defaultdict(list) #to lookup position of certain pieces
        self.whitepieces=[] #to iterate to all the pieces left
        self.blackpieces=[]
        if self.ruleset_=="classical":
            self.setup_board_classical(game)
    
    def setup_board_classical(self,game):
        whitepieces_=[Rook("white"),Knight("white"),Bishop("white"),Queen("white"),
                              King("white"),Bishop("white"),Knight("white"),Rook("white")]
        blackpieces_=[Rook("black"),Knight("black"),Bishop("black"),Queen("black"),
                              King("black"),Bishop("black"),Knight("black"),Rook("black")]
        for i in range(len(whitepieces_)):
            self.create_piece(7,i,whitepieces_[i])
            self.create_piece(0,i,blackpieces_[i])
            self.create_piece(6,i,Pawn("white"))
            self.create_piece(1,i,Pawn("black"))


            # self.append_piece_lookup(self.board[7][i])
            # self.append_piece_lookup(self.board[0][i])
            # self.append_piece_lookup(self.board[6][i])
            # self.append_piece_lookup(self.board[1][i])

            # self.append_whitepieces(self.board[7][i])
            # self.append_whitepieces(self.board[6][i])
            # self.append_blackpieces(self.board[0][i])
            # self.append_blackpieces(self.board[1][i])
        
    def deleting_piece(self,posy,posx): #delete it from all three datastructures
        p=self.board[posy][posx]
        if p==None:
            return
        self.remove_from_board(posy,posx)
   
        self.remove_piece_lookup(p)
        if p.color=="white":
        
            self.remove_whitepieces(p)
        elif p.color=="black":
            self.remove_blackpieces(p)
        return
        # key=(f"{self.board[posy][posx].symbol}_{self.board[posy][posx].color}")
        # # print("key:",key)
        # if key in self.piece_lookup:
        #     # print("key found")
        #     if isinstance(self.piece_lookup[key],list):
        #         # print("its a list")
        #         # print(self.piece_lookup[key])
        #         for piece_ in self.piece_lookup[key]:
        #             # print(piece_.position)
        #             if piece_.positiony==posy and piece_.positionx==posx:
        #                 if piece_.color=="white":
        #                     self.whitepieces.remove(piece_)
        #                 elif piece_.color=="black":
        #                     self.blackpieces.remove(piece_)
        #                     # print("how many blackpieces left:",len(self.blackpieces))
        #                 self.piece_lookup[key].remove(piece_)
        #                 self.board[posy][posx]==None
        #                 return  



    def make_move(self,move_): #updating the data structures for a complete move
        #for example the castle has 2 single moves
        # self.chessboard_.current_move=Rules.extract_moves_from_informations(piece,startrow,startcol,endrow,endcol,self.chessboard_.ruleset_,self.chessboard_,self.promotion_choice_)
        # for move in self.chessboard_.current_move:
        if move_.is_enpassant==False and move_.is_castle==False and move_.is_promotion==False:
            # print("normaler move")
            self.make_single_move(move_)
        elif move_.is_enpassant==True:
            self.make_single_move(move_)
            self.make_single_move(ChessMove(move_.captured_piece_posy,move_.captured_piece_posx,None,None,move_.captured_piece))
        elif move_.is_castle==True:
            self.make_single_move(move_)
            self.make_single_move(ChessMove(move_.castle_secondpiece_posy,move_.castle_secondpiece_posx,move_.startposy,(move_.startposx+move_.endposx)//2,move_.castle_secondpiece))
        elif move_.is_promotion==True:
            self.make_single_move(move_)
            p_move=ChessMove(move_.endposy,move_.endposx,None,None,move_.piece)
            self.make_single_move(p_move)
            # print("promo choice",move_.promotion_choice)
            self.make_single_move(ChessMove(None,None,move_.endposy,move_.endposx,move_.promotion_choice))
        self.append_move_list(move_)
        print("micro made a move")



    def make_single_move(self,move_): #updating the data structures for a single move
        if move_.endposy!=None and move_.endposx!=None and move_.startposy!=None and move_.startposx!=None: #normal move
            self.deleting_piece(move_.endposy,move_.endposx)
            self.deleting_piece(move_.startposy,move_.startposx)
            self.create_piece(move_.endposy,move_.endposx,move_.piece)
        if move_.endposy==None and move_.endposx==None and move_.startposy!=None and move_.startposx!=None: #delete a piece
            self.deleting_piece(move_.startposy,move_.startposx)
        if move_.startposy==None and move_.startposx==None and move_.endposx!=None and move_.endposy!=None: #spawn new piece
            self.create_piece(move_.endposy,move_.endposx,move_.piece)
        # if move_.startposy!=None and move_.startposx!=None: #always except new thing spawned
        #     self.board[move_.startposy][move_.startposx]=None

    def take_move_back(self,move_):
        if move_.is_enpassant==False and move_.is_castle==False and move_.is_promotion==False:
            self.take_single_move_back(move_)
            # print("before recreation of captured piece")
            if move_.captured_piece!=None:
                # print("recreation of captured piece")
                self.take_single_move_back(ChessMove(move_.captured_piece_posy,move_.captured_piece_posx,None,None,move_.captured_piece))
        elif move_.is_enpassant==True:
            self.take_single_move_back(move_)
            self.take_single_move_back(ChessMove(move_.captured_piece_posy,move_.captured_piece_posx,None,None,move_.captured_piece))
        elif move_.is_castle==True:
            self.take_single_move_back(move_)
            self.take_single_move_back(ChessMove(move_.captured_piece_posy,move_.captured_piece_posx,move_.startposy,(move_.startposx+move_.endposx)//2,move_.castle_secondpiece))
        elif move_.is_promotion==True:
            self.make_single_move(ChessMove(None,None,move_.endposy,move_.endposx,move_.promotion_choice))
            p_move=ChessMove(move_.endposy,move_.endposx,None,None,move_.piece)
            self.take_single_move_back(p_move)
            self.take_single_move_back(move_)
            if move_.captured_piece!=None:
                self.take_single_move_back(ChessMove(move_.captured_piece_posy,move_.captured_piece_posx,None,None,move_.captured_piece))
        self.pop_move_list()
            

    def take_single_move_back(self,move_):
        if move_.endposy!=None and move_.endposx!=None and move_.startposy!=None and move_.startposx!=None: #normal move
            self.deleting_piece(move_.endposy,move_.endposx)
            self.deleting_piece(move_.startposy,move_.startposx)
            self.create_piece(move_.startposy,move_.startposx,move_.piece)
        if move_.endposy==None and move_.endposx==None and move_.startposy!=None and move_.startposx!=None: #delete a piece
            self.create_piece(move_.startposy,move_.startposx,move_.piece)
            # print("takeback smth")
            # if move_.piece.symbol=="Q":
            #     print("takeback a queen")
        if move_.startposy==None and move_.startposx==None and move_.endposx!=None and move_.endposy!=None: #spawn new piece
            self.deleting_piece(move_.endposy,move_.endposx)
        # if move_.endposy!=None and move_.endposx!=None: #always except new thing spawned
        #     self.board[move_.endposy][move_.endposx]=None

    def create_piece(self,posy,posx,piece):
        # print("something created")
        piece.positiony=posy
        piece.positionx=posx
        self.add_to_board(piece,posy,posx)
        self.append_piece_lookup(piece)
        if piece.color=="white":
            self.append_whitepieces(piece)
        elif piece.color=="black":
            self.append_blackpieces(piece)

    ### methods to deal with database instead of objects

    def add_to_board(self,piece,posy,posx):
        l1=self.board
        if piece:
            piece=self.add_position_to_piece(piece,posy,posx)
        l1[posy][posx]=piece
        self.board=l1
   

    def remove_from_board(self,posy,posx):
        dic=self.board
        dic[posy][posx]=None
        self.board=dic

    def add_position_to_piece(self,piece,posy,posx):
        piece.positiony=posy
        piece.positionx=posx
        return piece
    
    def append_piece_lookup(self, piece):
        dict_=self.piece_lookup
        if piece:
            dict_[f"{piece.symbol}_{piece.color}"].append(piece)
        self.piece_lookup=dict_

    def remove_piece_lookup(self, piece):
        dict_=self.piece_lookup
        key=(f"{piece.symbol}_{piece.color}")
        if key in dict_:
            if isinstance(dict_[key],list):
                # print("its a list")
                # print(self.piece_lookup[key])
                for piece_ in dict_[key]:
                    # print(piece_.position)
                    if piece_.positiony==piece.positiony and piece_.positionx==piece.positionx:
                            # print("how many blackpieces left:",len(self.blackpieces))
                        dict_[key].remove(piece_)
                        self.piece_lookup=dict_


    def append_whitepieces(self,piece):
        l1=self.whitepieces
        l1.append(piece)
        self.whitepieces=l1

    def remove_whitepieces(self,piece):
        l1=self.whitepieces
        l1.remove(piece)
        self.whitepieces=l1

    def append_blackpieces(self,piece):
        l1=self.blackpieces
        l1.append(piece)
        self.blackpieces=l1

    def remove_blackpieces(self,piece):
        l1=self.blackpieces
        l1.remove(piece)
        self.blackpieces=l1

    def append_move_list(self, move):
        l1=self.move_list
        l1.append(move)
        self.move_list=l1

    def pop_move_list(self):
        l1=self.move_list
        l1.pop()
        self.move_list=l1