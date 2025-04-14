from base import Base
from sqlalchemy import Column, Integer, String, Boolean

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

class _ChessMove(Base):
    __tablename__ = 'chess_moves'

    id = Column(Integer, primary_key=True)
    startposy = Column(Integer)
    startposx = Column(Integer)
    endposy = Column(Integer)
    endposy = Column(Integer)
    piece = Column(String) ##noch json
    captured_piece = Column(String, nullable=True) ##noch json
    captured_piece_posy = Column(Integer, nullable=True)
    captured_piece_posx = Column(Integer, nullable=True)
    is_enpassant = Column(Boolean, default=False)
    is_castle = Column(Boolean, default=False)
    is_promotion = Column(Boolean, default=False)
    promotion_choice = Column(String, nullable=True) ##noch json
    castle_secondpiece = Column(String, nullable=True) ##noch json
    castle_secondpiece_posy = Column(Integer, nullable=True)
    castle_secondpiece_posx = Column(Integer, nullable=True)
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