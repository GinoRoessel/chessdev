from base import Base
from chesspieces import *
from chessmove import *
from collections import defaultdict
from itertools import chain

class ChessBoard:
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
        self.storage=None #to save a piece if you want to take the move back

    def create_board(self):
        self.board=[[None for _ in range(8)] for _ in range(8)] #main data structure
    
    def setup_board(self,game):
        self.board=[[None for _ in range(8)] for _ in range(8)]
        self.piece_lookup=defaultdict(list) #to lookup position of certain pieces
        self.whitepieces=[] #to iterate to all the pieces left
        self.blackpieces=[]
        self.storage=None
        self.storage_enpassant=None
        self.storage_gonepiece=None
        self.storage_promotedpiece=None
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
        # for item in self.whitepieces:
        #     print(item)
        #     print(item.position)

    # def listing_pieces(self):
    #     all_pieces = list(chain.from_iterable(
    #     [value] if not isinstance(value, list) else value
    #     for value in self.piece_lookup.values()  
    #     ))
    #     return all_pieces
        
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
                    
    # def update_board(self,move_):
    #     if move_.is_enpassant==False and move_.is_castle==False and move_.is_promotion==False:
    #         self.storage=self.board[move_.startposy][move_.startposx]
    #         self.storage_gonepiece=self.board[move_.endposy][move_.endposx]
    #         self.make_move(move_)
    #     elif move_.is_enpassant==True:
    #         ### hier weitermachen
    #         self.make_move(move_)
    #     elif move_.is_castle==True:
    #         self.make_move(move_)
    #     elif move_.is_promotion==True:
    #         self.make_move(move_)
        ##
        # self.storage=self.board[move__.endposy][move__.endposx]
        # self.deleting_piece((move__.endposy,move__.endposx))
        # self.board[move__.endposy][move__.endposx]=move__.piece
        # self.board[move__.startposy][move__.startposx]=None
        # move__.piece.position=(move__.endposy,move__.endposx)

    # def deupdate_board(self,move__):
    #     self.board[move__.startposy][move__.startposx]=self.board[move__.startposy][move__.startposx]=move__.piece
    #     move__.piece.position=(move__.startposy,move__.startposx)
    #     self.board[move__.endposy][move__.endposx]=self.storage
    #     if self.storage!=None:
    #         self.board[move__.endposy][move__.endposx].position=(move__.endposy,move__.endposx)
    #         self.piece_lookup[self.board[move__.endposy][move__.endposx].symbol,self.board[move__.endposy][move__.endposx].color].append(self.board[move__.endposy][move__.endposx])
    #         if self.board[move__.endposy][move__.endposx].color=="white":
    #             self.whitepieces.append(self.board[move__.endposy][move__.endposx])
    #         elif self.board[move__.endposy][move__.endposx].color=="black":
    #             self.blackpieces.append(self.board[move__.endposy][move__.endposx])


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