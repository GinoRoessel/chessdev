from database.base import Base
from sqlalchemy import Column, Integer, String, Boolean
from chesspieces import *
from chessmove import *


class ChessGameData(Base):
    __tablename__ = 'chessgame_data'
    id = Column(Integer, primary_key=True)
    ruleset_=Column(String)
    _selected_piece=Column("selected_piece",String,nullable=True) 
    selected_posy=Column(Integer,nullable=True)
    selected_posx=Column(Integer,nullable=True)
    current_player=Column(String)
    status=Column(String,nullable=True)
    chessgame_ended=Column(Boolean, default=False)




    def __init__(self):

        self._selected_piece=None

        self.ruleset_="classical"
        self.selected_piece=None
        self.selected_posy=None
        self.selected_posx=None
        self.current_player="white"
        self.status=" "
        self.chessgame_ended=False


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

