from base import Base
class _ChessPieces:
    def __init__(self,color,symbol,guisymbol):
        self.color=color
        self.guisymbol=guisymbol #unicode
        self.position=None
        self.symbol=symbol #letter
    
    def __str__(self):
        return self.guisymbol
    
class ChessPieces:
    def __init__(self,color,symbol,guisymbol):
        self.color=color
        self.guisymbol=guisymbol #unicode
        self.positionx=None
        self.positiony=None
        self.symbol=symbol #letter
    
    def __str__(self):
        return self.guisymbol
    
        
class Queen(ChessPieces):
    def __init__(self,color):
        super().__init__(color,"Q","\u265B")

class King(ChessPieces):
    def __init__(self,color):
        super().__init__(color,"K","\u265A")

class Pawn(ChessPieces):
    def __init__(self,color):
        super().__init__(color,"P","\u265F")

class Bishop(ChessPieces):
    def __init__(self,color):
        super().__init__(color,"B","\u265D")

class Knight(ChessPieces):
    def __init__(self,color):
        super().__init__(color,"N","\u265E")

class Rook(ChessPieces):
    def __init__(self,color):
        super().__init__(color,"R","\u265C")