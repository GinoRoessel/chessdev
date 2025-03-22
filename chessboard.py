from chesspieces import *
from collections import defaultdict
from itertools import chain

class ChessBoard:
    def __init__(self):
        self.create_board()
        self.piece_lookup=defaultdict(list) #to lookup position of certain pieces
        self.whitepieces=[] #to iterate to all the pieces left
        self.blackpieces=[]
        self.storage=None #to save a piece if you want to take the move back

    def create_board(self):
        self.board=[[None for _ in range(8)] for _ in range(8)] #main data structure
    
    def setup_board(self,ruleset,game):
        if ruleset=="classical":
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
            self.board[7][i].position=(7,i) 
            self.board[6][i].position=(6,i)
            self.board[1][i].position=(1,i)
            self.board[0][i].position=(0,i)
            # print(self.board[0][i])
            # print(self.board[0][i].position)
            if not isinstance(whitepieces_[i],King):
                self.piece_lookup[self.board[7][i].symbol,"white"].append(self.board[7][i]) #adding to the lookup_dict
                self.piece_lookup[self.board[0][i].symbol,"black"].append(self.board[0][i])
            else:
                self.piece_lookup[self.board[7][i].symbol,"white"]=(self.board[7][i])
                self.piece_lookup[self.board[0][i].symbol,"black"]=(self.board[0][i])
            self.piece_lookup[self.board[6][i].symbol,"white"].append(self.board[6][i])
            self.piece_lookup[self.board[1][i].symbol,"black"].append(self.board[1][i])
            self.whitepieces.append(self.board[7][i]) #adding to the simple list
            self.whitepieces.append(self.board[6][i])
            self.blackpieces.append(self.board[0][i])
            self.blackpieces.append(self.board[1][i])
        # for item in self.whitepieces:
        #     print(item)
        #     print(item.position)

    # def listing_pieces(self):
    #     all_pieces = list(chain.from_iterable(
    #     [value] if not isinstance(value, list) else value
    #     for value in self.piece_lookup.values()  
    #     ))
    #     return all_pieces
        
    def deleting_piece(self,pos): #delete it from all three datastructures
        if self.board[pos[0]][pos[1]]==None:
            return
        key=(self.board[pos[0]][pos[1]].symbol,self.board[pos[0]][pos[1]].color)
        print(key)
        if key in self.piece_lookup:
            # print("key found")
            if isinstance(self.piece_lookup[key],list):
                # print("its a list")
                # print(self.piece_lookup[key])
                for piece_ in self.piece_lookup[key]:
                    # print(piece_.position)
                    if piece_.position==pos:
                        if piece_.color=="white":
                            self.whitepieces.remove(piece_)
                        elif piece_.color=="black":
                            self.blackpieces.remove(piece_)
                            print(len(self.blackpieces))
                        self.piece_lookup[key].remove(piece_)
                        return
                    
    def update_board(self,piece,startrow,startcol,endrow,endcol):
        self.storage=self.board[endrow][endcol]
        self.deleting_piece((endrow,endcol))
        self.board[endrow][endcol]=piece
        self.board[startrow][startcol]=None
        piece.position=(endrow,endcol)

    def deupdate_board(self,piece,startrow,startcol,endrow,endcol):
        self.board[startrow][startcol]=self.board[startrow][startcol]=piece
        piece.position=(startrow,startcol)
        self.board[endrow][endcol]=self.storage
        if self.storage!=None:
            self.board[endrow][endcol].position=(endrow,endcol)
            self.piece_lookup[self.board[endrow][endcol].symbol,self.board[endrow][endcol].color].append(self.board[endrow][endcol])
            if self.board[endrow][endcol].color=="white":
                self.whitepieces.append(self.board[endrow][endcol])
            elif self.board[endrow][endcol].color=="black":
                self.blackpieces.append(self.board[endrow][endcol])