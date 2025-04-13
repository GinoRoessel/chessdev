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
        self.selected_pos=None
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
            self.board[7][i].position=(7,i) 
            self.board[6][i].position=(6,i)
            self.board[1][i].position=(1,i)
            self.board[0][i].position=(0,i)
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
        
    def deleting_piece(self,pos): #delete it from all three datastructures
        if self.board[pos[0]][pos[1]]==None:
            return
        key=(self.board[pos[0]][pos[1]].symbol,self.board[pos[0]][pos[1]].color)
        print("key:",key)
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
                            print("how many blackpieces left:",len(self.blackpieces))
                        self.piece_lookup[key].remove(piece_)
                        return
                    
    # def update_board(self,move_):
    #     if move_.is_enpassant==False and move_.is_castle==False and move_.is_promotion==False:
    #         self.storage=self.board[move_.startpos[0]][move_.startpos[1]]
    #         self.storage_gonepiece=self.board[move_.endpos[0]][move_.endpos[1]]
    #         self.make_move(move_)
    #     elif move_.is_enpassant==True:
    #         ### hier weitermachen
    #         self.make_move(move_)
    #     elif move_.is_castle==True:
    #         self.make_move(move_)
    #     elif move_.is_promotion==True:
    #         self.make_move(move_)
        ##
        # self.storage=self.board[move__.endpos[0]][move__.endpos[1]]
        # self.deleting_piece((move__.endpos[0],move__.endpos[1]))
        # self.board[move__.endpos[0]][move__.endpos[1]]=move__.piece
        # self.board[move__.startpos[0]][move__.startpos[1]]=None
        # move__.piece.position=(move__.endpos[0],move__.endpos[1])

    # def deupdate_board(self,move__):
    #     self.board[move__.startpos[0]][move__.startpos[1]]=self.board[move__.startpos[0]][move__.startpos[1]]=move__.piece
    #     move__.piece.position=(move__.startpos[0],move__.startpos[1])
    #     self.board[move__.endpos[0]][move__.endpos[1]]=self.storage
    #     if self.storage!=None:
    #         self.board[move__.endpos[0]][move__.endpos[1]].position=(move__.endpos[0],move__.endpos[1])
    #         self.piece_lookup[self.board[move__.endpos[0]][move__.endpos[1]].symbol,self.board[move__.endpos[0]][move__.endpos[1]].color].append(self.board[move__.endpos[0]][move__.endpos[1]])
    #         if self.board[move__.endpos[0]][move__.endpos[1]].color=="white":
    #             self.whitepieces.append(self.board[move__.endpos[0]][move__.endpos[1]])
    #         elif self.board[move__.endpos[0]][move__.endpos[1]].color=="black":
    #             self.blackpieces.append(self.board[move__.endpos[0]][move__.endpos[1]])


    def make_move(self,move_): #updating the data structures for a complete move
        #for example the castle has 2 single moves
        # self.chessboard_.current_move=Rules.extract_moves_from_informations(piece,startrow,startcol,endrow,endcol,self.chessboard_.ruleset_,self.chessboard_,self.promotion_choice_)
        # for move in self.chessboard_.current_move:
        if move_.is_enpassant==False and move_.is_castle==False and move_.is_promotion==False:
            self.make_single_move(move_)
        elif move_.is_enpassant==True:
            self.make_single_move(move_)
            self.make_single_move(ChessMove(move_.captured_piece_pos,(None,None),move_.captured_piece))
        elif move_.is_castle==True:
            self.make_single_move(move_)
            self.make_single_move(ChessMove(move_.castle_secondpiece_pos,(move_.startpos[0],(move_.startpos[1]+move_.endpos[1])//2),move_.castle_secondpiece))
        elif move_.is_promotion==True:
            self.make_single_move(move_)
            p_move=ChessMove(move_.endpos,(None,None),move_.piece)
            self.make_single_move(p_move)
            print("promo choice",move_.promotion_choice)
            self.make_single_move(ChessMove((None,None),move_.endpos,move_.promotion_choice))
        self.move_list.append(move_)



    def make_single_move(self,move_): #updating the data structures for a single move
        if move_.endpos[0]!=None and move_.endpos[1]!=None and move_.startpos[0]!=None and move_.startpos[1]!=None: #normal move
            self.deleting_piece((move_.endpos[0],move_.endpos[1]))
            self.board[move_.endpos[0]][move_.endpos[1]]=move_.piece
            self.board[move_.endpos[0]][move_.endpos[1]].position=(move_.endpos[0],move_.endpos[1])
        if move_.endpos[0]==None and move_.endpos[1]==None and move_.startpos[0]!=None and move_.startpos[1]!=None: #delete a piece
            self.deleting_piece((move_.startpos[0],move_.startpos[1]))
        if move_.startpos[0]==None and move_.startpos[1]==None and move_.endpos[1]!=None and move_.endpos[0]!=None: #spawn new piece
            self.board[move_.endpos[0]][move_.endpos[1]]=move_.piece
            print(move_.piece)
            self.board[move_.endpos[0]][move_.endpos[1]].position=(move_.endpos[0],move_.endpos[1])
            self.piece_lookup[self.board[move_.endpos[0]][move_.endpos[1]].symbol,self.board[move_.endpos[0]][move_.endpos[1]].color].append(self.board[move_.endpos[0]][move_.endpos[1]])
            if move_.piece.color=="white":
                self.whitepieces.append(self.board[move_.endpos[0]][move_.endpos[1]])
            else:
                self.blackpieces.append(self.board[move_.endpos[0]][move_.endpos[1]])
        if move_.startpos[0]!=None and move_.startpos[1]!=None: #always except new thing spawned
            self.board[move_.startpos[0]][move_.startpos[1]]=None

    def take_move_back(self,move_):
        if move_.is_enpassant==False and move_.is_castle==False and move_.is_promotion==False:
            self.take_single_move_back(move_)
            if move_.captured_piece!=None:
                self.take_single_move_back(ChessMove(move_.captured_piece_pos,(None,None),move_.captured_piece))
        elif move_.is_enpassant==True:
            self.take_single_move_back(move_)
            self.take_single_move_back(ChessMove(move_.captured_piece_pos,(None,None),move_.captured_piece))
        elif move_.is_castle==True:
            self.take_single_move_back(move_)
            self.take_single_move_back(ChessMove(move_.castle_secondpiece_pos,(move_.startpos[0],(move_.startpos[1]+move_.endpos[1])//2),move_.castle_secondpiece))
        elif move_.is_promotion==True:
            self.make_single_move(ChessMove((None,None),move_.endpos,move_.promotion_choice))
            p_move=ChessMove(move_.endpos,(None,None),move_.piece)
            self.take_single_move_back(p_move)
            self.take_single_move_back(move_)
            if move_.captured_piece!=None:
                self.take_single_move_back(ChessMove(move_.captured_piece_pos,(None,None),move_.captured_piece))
        self.move_list.pop()
            

    def take_single_move_back(self,move_):
        if move_.endpos[0]!=None and move_.endpos[1]!=None and move_.startpos[0]!=None and move_.startpos[1]!=None: #normal move
            self.board[move_.startpos[0]][move_.startpos[1]]=move_.piece
            self.board[move_.startpos[0]][move_.startpos[1]].position=(move_.startpos[0],move_.startpos[1])
            self.board[move_.endpos[0]][move_.endpos[1]]=None
        if move_.endpos[0]==None and move_.endpos[1]==None and move_.startpos[0]!=None and move_.startpos[1]!=None: #delete a piece
            self.create_piece((move_.startpos[0],move_.startpos[1]),move_.piece)
        if move_.startpos[0]==None and move_.startpos[1]==None and move_.endpos[1]!=None and move_.endpos[0]!=None: #spawn new piece
            self.deleting_piece(move_.endpos)
        if move_.endpos[0]!=None and move_.endpos[1]!=None: #always except new thing spawned
            self.board[move_.endpos[0]][move_.endpos[1]]=None

    def create_piece(self,pos,piece):
        self.board[pos[0]][pos[1]]=piece
        self.board[pos[0]][pos[1]].position=(pos[0],pos[1])
        self.piece_lookup[self.board[pos[0]][pos[1]].symbol,self.board[pos[0]][pos[1]].color].append(self.board[pos[0]][pos[1]])
        if piece.color=="white":
            self.whitepieces.append(self.board[pos[0]][pos[1]])
        else:
            self.blackpieces.append(self.board[pos[0]][pos[1]])