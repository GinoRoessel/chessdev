from base import Base
from sqlalchemy import Column, Integer, String, Boolean
from chesspieces import ChessPieces
import json

class ChessMove():
    def __init__(self,startposy,startposx,endposy,endposx,piece,captured_piece=None,captured_piece_posy=None,captured_piece_posx=None,
                 is_enpassant=False,is_castle=False,is_promotion=False,promotion_choice=None,
                 castle_secondpiece=None,castle_secondpiece_posy=None,castle_secondpiece_posx=None):
        self.startposy=startposy
        self.startposx=startposx
        self.endposy=endposy
        self.endposx=endposx
        self.piece=piece
        self.captured_piece=captured_piece
        self.captured_piece_posy=captured_piece_posy
        self.captured_piece_posx=captured_piece_posx
        self.is_enpassant=is_enpassant
        self.is_castle=is_castle
        self.is_promotion=is_promotion
        self.promotion_choice=promotion_choice
        self.castle_secondpiece=castle_secondpiece
        self.castle_secondpiece_posy=castle_secondpiece_posy
        self.castle_secondpiece_posx=castle_secondpiece_posx

    def to_dict(self):
        return {"startposy":self.startposy,
        "startposx":self.startposx,
        "endposy":self.endposy,
        "endposx":self.endposx,
        "piece":self.piece,
        "captured_piece":self.captured_piece,
        "captured_piece_posy":self.captured_piece_posy,
        "captured_piece_posx":self.captured_piece_posx,
        "is_enpassant":self.is_enpassant,
        "is_castle":self.is_castle,
        "is_promotion":self.is_promotion,
        "promotion_choice":self.promotion_choice,
        "castle_secondpiece":self.castle_secondpiece,
        "castle_secondpiece_posy":self.castle_secondpiece_posy,
        "castle_secondpiece_posx":self.castle_secondpiece_posx
        }

    @classmethod
    def from_dict(cls,dict):
        return cls(
            startposy=dict["startposy"],
            startposx=dict["startposx"],
            endposy=dict["endposy"],
            endposx=dict["endposx"],
            piece=dict["piece"],
            captured_piece=dict["captured_piece"],
            captured_piece_posy=dict["captured_piece_posy"],
            captured_piece_posx=dict["captured_piece_posx"],
            is_enpassant=dict["is_enpassant"],
            is_castle=dict["is_castle"],
            is_promotion=dict["is_promotion"],
            promotion_choice=dict["promotion_choice"],
            castle_secondpiece=dict["castle_secondpiece"],
            castle_secondpiece_posy=dict["castle_secondpiece_posy"],
            castle_secondpiece_posx=dict["castle_secondpiece_posx"]
            )
            

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_):
        dict=json.loads(json_)
        return cls.from_dict(dict)

class _ChessMove(Base):
    __tablename__ = 'chess_moves'

    id = Column(Integer, primary_key=True)
    startposy = Column(Integer)
    startposx = Column(Integer)
    endposy = Column(Integer)
    endposx = Column(Integer)
    piece = Column(String) 
    captured_piece = Column(String, nullable=True) 
    captured_piece_posy = Column(Integer, nullable=True)
    captured_piece_posx = Column(Integer, nullable=True)
    is_enpassant = Column(Boolean, default=False)
    is_castle = Column(Boolean, default=False)
    is_promotion = Column(Boolean, default=False)
    promotion_choice = Column(String, nullable=True) 
    castle_secondpiece = Column(String, nullable=True) 
    castle_secondpiece_posy = Column(Integer, nullable=True)
    castle_secondpiece_posx = Column(Integer, nullable=True)
    def __init__(self,startposy,startposx,endposy,endposx,piece,captured_piece=None,captured_piece_posy=None,captured_piece_posx=None,
                 is_enpassant=False,is_castle=False,is_promotion=False,promotion_choice=None,
                 castle_secondpiece=None,castle_secondpiece_posy=None,castle_secondpiece_posx=None):
        
        self._piece = None 
        self._captured_piece = None 
        self._promotion_choice = None  
        self._castle_second_piece = None  

        self.startposy=startposy
        self.startposx=startposx
        self.endposy=endposy
        self.endposx=endposx
        self.piece=piece
        self.captured_piece=captured_piece
        self.captured_piece_posy=captured_piece_posy
        self.captured_piece_posx=captured_piece_posx
        self.is_enpassant=is_enpassant
        self.is_castle=is_castle
        self.is_promotion=is_promotion
        self.promotion_choice=promotion_choice
        self.castle_secondpiece=castle_secondpiece
        self.castle_secondpiece_posy=castle_secondpiece_posy
        self.castle_secondpiece_posx=castle_secondpiece_posx

    @property
    def piece(self):
        if self._piece:
            return ChessPieces.from_json(self._piece)
        else:
            return None
    
    @piece.setter
    def piece(self, piece_):
        if piece_:
            self._piece=piece_.to_json()
        else:
            self._piece=None

    @property
    def captured_piece(self):
        if self._captured_piece:
            return ChessPieces.from_json(self._captured_piece)
        else:
            return None
    
    @captured_piece.setter
    def captured_piece(self, piece_):
        if piece_:
            self._captured_piece=piece_.to_json()
        else:
            self._captured_piece=None

    @property
    def promotion_choice(self):
        if self._promotion_choice:
            return ChessPieces.from_json(self._promotion_choice)
        else: 
            return None
    
    @promotion_choice.setter
    def promotion_choice(self, piece_):
        if piece_:
            self._promotion_choice=piece_.to_json()
        else:
            self._promotion_choice=None

    @property
    def castle_second_piece(self):
        if self._castle_second_piece:
            return ChessPieces.from_json(self._castle_second_piece)
        else:
            return None
    
    @castle_second_piece.setter
    def castle_second_piece(self, piece_):
        if piece_:
            self._castle_second_piece=piece_.to_json()
        else:
            self._castle_second_piece=None

    def to_dict(self):
        return {"startposy":self.startposy,
        "startposx":self.startposx,
        "endposy":self.endposy,
        "endposx":self.endposx,
        "piece":self.piece,
        "captured_piece":self.captured_piece,
        "captured_piece_posy":self.captured_piece_posy,
        "captured_piece_posx":self.captured_piece_posx,
        "is_enpassant":self.is_enpassant,
        "is_castle":self.is_castle,
        "is_promotion":self.is_promotion,
        "promotion_choice":self.promotion_choice,
        "castle_secondpiece":self.castle_secondpiece,
        "castle_secondpiece_posy":self.castle_secondpiece_posy,
        "castle_secondpiece_posx":self.castle_secondpiece_posx
        }

    @classmethod
    def from_dict(cls,dict):
        return cls(
            startposy=dict["startposy"],
            startposx=dict["startposx"],
            endposy=dict["endposy"],
            endposx=dict["endposx"],
            piece=dict["piece"],
            captured_piece=dict["captured_piece"],
            captured_piece_posy=dict["captured_piece_posy"],
            captured_piece_posx=dict["captured_piece_posx"],
            is_enpassant=dict["is_enpassant"],
            is_castle=dict["is_castle"],
            is_promotion=dict["is_promotion"],
            promotion_choice=dict["promotion_choice"],
            castle_secondpiece=dict["castle_secondpiece"],
            castle_secondpiece_posy=dict["castle_secondpiece_posy"],
            castle_secondpiece_posx=dict["castle_secondpiece_posx"]
            )
            

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_):
        dict=json.loads(json_)
        return cls.from_dict(dict)