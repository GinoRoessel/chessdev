from database.base import Base
from sqlalchemy import Column, Integer, String, Boolean
from chesspieces import *
from chessmove import *
from collections import defaultdict
from itertools import chain

class ChessBoard(Base):
    __tablename__ = 'chess_boards'

    id = Column(Integer, primary_key=True, autoincrement=True)
    gamedata_id=Column(Integer)
    _board=Column("board",String) 
    _piece_lookup=Column("piece_lookup",String,nullable=True) 
    _whitepieces=Column("whitepieces",String,nullable=True) 
    _blackpieces=Column("blackpieces",String,nullable=True) 
    _current_move=Column("current_move",String,nullable=True)
    is_replay=Column(Boolean,default=False)
    

    def __init__(self,gamedata_id,is_replay=False):
        self.gamedata_id=gamedata_id
        self._whitepieces=None
        self._blackpieces=None
        self._piece_lookup=None
        self._board=None
        self._current_move=None

        self.create_board() #just create the matrix
        self.piece_lookup=defaultdict(list) #to lookup position of certain pieces
        self.whitepieces=[] #to iterate to all the pieces of the color
        self.blackpieces=[]
        self.current_move=None
        self.is_replay=is_replay

    

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

    def create_board(self):
        self.board=[[None for _ in range(8)] for _ in range(8)] #main data structure
    
    def setup_board(self,game,ruleset): #setup the pieces on all datastructures
        self.board=[[None for _ in range(8)] for _ in range(8)]
        if ruleset=="classical":
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
        
    def deleting_piece(self,posy,posx): #delete it from all datastructures
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



    def make_move(self,session,move_): #updating the data structures for a complete move
        #for example the castle has 2 single moves
        if move_.is_enpassant==False and move_.is_castle==False and move_.is_promotion==False: #normal move
            self.make_single_move(move_)
        elif move_.is_enpassant==True: #enpassant
            self.make_single_move(move_)
            self.make_single_move(lightChessMove(self.id,move_.captured_piece_posy,move_.captured_piece_posx,None,None,move_.captured_piece))
        elif move_.is_castle==True: #castle
            self.make_single_move(move_)
            self.make_single_move(lightChessMove(self.id,move_.castle_secondpiece_posy,move_.castle_secondpiece_posx,move_.startposy,(move_.startposx+move_.endposx)//2,move_.castle_secondpiece))
        elif move_.is_promotion==True: #promotion
            self.make_single_move(move_)
            p_move=lightChessMove(self.id,self.id,move_.endposy,move_.endposx,None,None,move_.piece)
            self.make_single_move(p_move)
            # print("promo choice",move_.promotion_choice)
            self.make_single_move(lightChessMove(self.id,None,None,move_.endposy,move_.endposx,move_.promotion_choice))
        # session.add(move_)
        # session.commit()
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

    def take_move_back(self,session,move_): #counterpart of make_move
        if move_.is_enpassant==False and move_.is_castle==False and move_.is_promotion==False: #normal move
            self.take_single_move_back(move_)
            # print("before recreation of captured piece")
            if move_.captured_piece!=None:
                # print("recreation of captured piece")
                self.take_single_move_back(lightChessMove(self.id,move_.captured_piece_posy,move_.captured_piece_posx,None,None,move_.captured_piece))
        elif move_.is_enpassant==True: #enpassant
            self.take_single_move_back(move_)
            self.take_single_move_back(lightChessMove(self.id,move_.captured_piece_posy,move_.captured_piece_posx,None,None,move_.captured_piece))
        elif move_.is_castle==True: #castle
            self.take_single_move_back(move_)
            self.take_single_move_back(lightChessMove(self.id,move_.captured_piece_posy,move_.captured_piece_posx,move_.startposy,(move_.startposx+move_.endposx)//2,move_.castle_secondpiece))
        elif move_.is_promotion==True: #promotion
            self.make_single_move(lightChessMove(self.id,None,None,move_.endposy,move_.endposx,move_.promotion_choice))
            p_move=lightChessMove(self.id,move_.endposy,move_.endposx,None,None,move_.piece)
            self.take_single_move_back(p_move)
            self.take_single_move_back(move_)
            if move_.captured_piece!=None:
                self.take_single_move_back(lightChessMove(self.id,move_.captured_piece_posy,move_.captured_piece_posx,None,None,move_.captured_piece))
        # last_move = session.query(ChessMove).filter_by(board_id=self.id).order_by(ChessMove.id.desc()).first()
        # if last_move:
        #     session.delete(last_move)
        #     session.commit()
        # self.pop_move_list()
            

    def take_single_move_back(self,move_):
        if move_.endposy!=None and move_.endposx!=None and move_.startposy!=None and move_.startposx!=None: #normal move
            self.deleting_piece(move_.endposy,move_.endposx)
            self.deleting_piece(move_.startposy,move_.startposx)
            self.create_piece(move_.startposy,move_.startposx,move_.piece)
        if move_.endposy==None and move_.endposx==None and move_.startposy!=None and move_.startposx!=None: #delete a piece-> spawn
            self.create_piece(move_.startposy,move_.startposx,move_.piece)
            # print("takeback smth")
            # if move_.piece.symbol=="Q":
            #     print("takeback a queen")
        if move_.startposy==None and move_.startposx==None and move_.endposx!=None and move_.endposy!=None: #spawn new piece-> delete
            self.deleting_piece(move_.endposy,move_.endposx)
        # if move_.endposy!=None and move_.endposx!=None: #always except new thing spawned
        #     self.board[move_.endposy][move_.endposx]=None

    def create_piece(self,posy,posx,piece): #create it in all data structures
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
