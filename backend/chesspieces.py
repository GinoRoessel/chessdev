from base import Base
import json
class ChessPieces:
    def __init__(self,color,symbol,guisymbol,positiony=None,positionx=None):
        self.color=color
        self.guisymbol=guisymbol #unicode
        self.positionx=positionx
        self.positiony=positiony
        self.symbol=symbol #letter

    def __eq__(self, other):
        if not isinstance(other, ChessPieces):
            return False
        return (
            self.color == other.color and
            self.symbol == other.symbol and
            self.positionx == other.positionx and
            self.positiony == other.positiony and 
            self.guisymbol == other.guisymbol
        )
    
    def __str__(self):
        return self.guisymbol
    
    def to_dict(self):
        return {"color":self.color,
                "guisymbol":self.guisymbol,
                "positiony":self.positiony,
                "positionx":self.positionx,
                "symbol":self.symbol
        }
    
    @staticmethod
    def from_dict(dict):
        if dict==None:
            return None
        symb=dict["symbol"]
        if symb=="P":
            return Pawn(color=dict["color"],
                positionx=dict["positionx"],
                positiony=dict["positiony"])
        elif symb=="R":
            return Rook(color=dict["color"],
                positionx=dict["positionx"],
                positiony=dict["positiony"]) 
        elif symb=="B":
            return Bishop(color=dict["color"],
                positionx=dict["positionx"],
                positiony=dict["positiony"])   
        elif symb=="N":
            return Knight(color=dict["color"],
                positionx=dict["positionx"],
                positiony=dict["positiony"])
        elif symb=="K":
            return King(color=dict["color"],
                positionx=dict["positionx"],
                positiony=dict["positiony"])
        elif symb=="Q":
            return Queen(color=dict["color"],
                positionx=dict["positionx"],
                positiony=dict["positiony"])

        
    def to_json(self):
        return json.dumps(self.to_dict())
        
    @classmethod
    def from_json(cls, json_):
        dict_=json.loads(json_)
        return ChessPieces.from_dict(dict_)
    
        
class Queen(ChessPieces):
    def __init__(self,color,positiony=None,positionx=None):
        super().__init__(color,"Q","\u265B",positiony,positionx)

class King(ChessPieces):
    def __init__(self,color,positiony=None,positionx=None):
        super().__init__(color,"K","\u265A",positiony,positionx)

class Pawn(ChessPieces):
    def __init__(self,color,positiony=None,positionx=None):
        super().__init__(color,"P","\u265F",positiony,positionx)

class Bishop(ChessPieces):
    def __init__(self,color,positiony=None,positionx=None):
        super().__init__(color,"B","\u265D",positiony,positionx)

class Knight(ChessPieces):
    def __init__(self,color,positiony=None,positionx=None):
        super().__init__(color,"N","\u265E",positiony,positionx)

class Rook(ChessPieces):
    def __init__(self,color,positiony=None,positionx=None):
        super().__init__(color,"R","\u265C",positiony,positionx)