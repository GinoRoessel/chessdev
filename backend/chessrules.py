from chesspieces import *
from chessmove import *
#

class Rules: #just staticmethods
    def __init__(self,ruleset):
        pass

            
    @staticmethod #complete check of a move
    def is_valid_move(move__,board,promotion_choice=None,justtest=False):
        move_=Rules.is_possible_move(move__,board,justtest)
        if not move_:
            return False
        move_=Rules.testing_move(move_,board,promotion_choice,justtest)
        if not move_:
            return False
        # print("valid")

        return move_
    
    @staticmethod #if the logic of the piece would allow the move
    def is_possible_move(move__,board,justtest=False):
        if board.ruleset_=="classical":
            if Rules.is_own_piece(move__,board) is True:
                print("is an own piece")
                return False
            if (move__.startposy,move__.startposx)==(move__.endposy,move__.endposx):
                print("not changed the position")
                return False
            if isinstance(move__.piece,Pawn):
                return Rules.is_possible_pawnmove_classical(move__,board,justtest)
            elif isinstance(move__.piece,Rook):
                return Rules.is_possible_rookmove_classical(move__,board,justtest)
            elif isinstance(move__.piece,Knight):
                return Rules.is_possible_knightmove_classical(move__,board,justtest)
            elif isinstance(move__.piece,Bishop):
                return Rules.is_possible_bishopmove_classical(move__,board,justtest)
            elif isinstance(move__.piece,Queen):
                return Rules.is_possible_queenmove_classical(move__,board,justtest)
            elif isinstance(move__.piece,King):
                return Rules.is_possible_kingmove_classical(move__,board,justtest)

    @staticmethod
    def is_possible_pawnmove_classical(move__,board,justtest):
        # print("piece is",piece)
        # print("startrow is",startrow)
        # print("startcol is",startcol)
        # print("endrow is",endrow)
        # print("endcol is",endcol)
        direction=-1 if move__.piece.color=="white" else 1
        if move__.startposx==move__.endposx: #geradeaus
            if move__.endposy-move__.startposy==direction and board.board[move__.endposy][move__.endposx] is None: #ein Feld
                if move__.endposy==0 or move__.endposy==7:
                    move__.is_promotion=True
                return move__
            if move__.endposy-move__.startposy==2*direction and move__.startposy==(6 if move__.piece.color == "white" else 1)\
                and board.board[move__.endposy][move__.endposx] is None and board.board[(move__.endposy+move__.startposy)//2][move__.endposx] is None: #zwei Felder
                return move__
        try: 
            if (move__.startposx+1==move__.endposx or move__.startposx-1==move__.endposx) and move__.endposy-move__.startposy==direction\
              and board.board[move__.endposy][move__.endposx].color!=move__.piece.color: #diagonal schlagen
                move__.captured_piece=board.board[move__.endposy][move__.endposx]
                move__.captured_piece_posy=move__.endposy
                move__.captured_piece_posx=move__.endposx
                if move__.endposy==0 or move__.endposy==7:
                    move__.is_promotion=True
                return move__
        except AttributeError:
            pass
        #en passant
        try:
            if (move__.startposx+1==move__.endposx or move__.startposx-1==move__.endposx)\
            and move__.endposy-move__.startposy==direction\
            and move__.startposy==(3 if move__.piece.color=="white" else 4)\
            and board.board[move__.startposy][move__.endposx].color!=move__.piece.color\
            and board.move_list[-1].endposy==move__.startposy\
            and board.move_list[-1].endposx==move__.endposx:
                move__.captured_piece=board.board[move__.startposy][move__.endposx]
                move__.captured_piece_posy=move__.startposy
                move__.captured_piece_posx=move__.endposx
                move__.is_enpassant=True
                return move__
        except AttributeError:
            pass

        return False
            

    @staticmethod
    def is_possible_rookmove_classical(move__,board,justtest):
        if move__.startposy==move__.endposy or move__.startposx==move__.endposx:
            return Rules.is_path_clear_rook_classical(move__,board,justtest)
        return False

    def is_path_clear_rook_classical(move__,board,justtest):
        if move__.startposy==move__.endposy:
            direction=1 if move__.startposx<move__.endposx else -1
            # if abs(endcol-startcol)==1:
            #     return True
            for i in range(1,abs(move__.endposx-move__.startposx)):
                if board.board[move__.startposy][move__.startposx+(i*direction)] is not None:
                    return False
            
            move__.captured_piece=board.board[move__.endposy][move__.endposx]
            move__.captured_piece_posy=move__.endposy
            move__.captured_piece_posx=move__.endposx
            return move__  
        if move__.startposx==move__.endposx:
            direction=1 if move__.startposy<move__.endposy else -1
            # if abs(endrow-startrow)==1:
            #     return True
            for i in range(1,abs(move__.endposy-move__.startposy)):
                if board.board[move__.startposy+(i*direction)][move__.startposx] is not None:
                    return False
            
            move__.captured_piece=board.board[move__.endposy][move__.endposx]
            move__.captured_piece_posy=move__.endposy
            move__.captured_piece_posx=move__.endposx
            return move__      
        return False
#
    @staticmethod
    def is_possible_knightmove_classical(move__,board,justtest):
        if (abs(move__.startposy-move__.endposy)==2 or abs(move__.startposy-move__.endposy)==1) and \
        (abs(move__.startposx-move__.endposx)==2 or abs(move__.startposx-move__.endposx)==1) and \
        (abs(move__.startposy-move__.endposy)+abs(move__.startposx-move__.endposx)==3):
    
            move__.captured_piece=board.board[move__.endposy][move__.endposx]
            move__.captured_piece_posy=move__.endposy
            move__.captured_piece_posx=move__.endposx
            return move__
        else:
            return False

    @staticmethod
    def is_possible_bishopmove_classical(move__,board,justtest):
        if abs(move__.startposy-move__.endposy)==abs(move__.startposx-move__.endposx):
            return Rules.is_path_clear_bishop_classical(move__,board,justtest)
        else: 
            return False
        
    def is_path_clear_bishop_classical(move__,board,justtest):
        if move__.startposy>move__.endposy and move__.startposx>move__.endposx:
            direction=(-1,-1)
        elif move__.startposy>move__.endposy and move__.startposx<move__.endposx:
            direction=(-1,1)
        elif move__.startposy<move__.endposy and move__.startposx>move__.endposx:
            direction=(1,-1)
        elif move__.startposy<move__.endposy and move__.startposx<move__.endposx:
            direction=(1,1)
        for i in range(1,abs(move__.startposy-move__.endposy)):
            if board.board[move__.startposy+(direction[0]*i)][move__.startposx+(direction[1]*i)] is not None:
                return False
        move__.captured_piece=board.board[move__.endposy][move__.endposx]
        move__.captured_piece_posy=move__.endposy
        move__.captured_piece_posx=move__.endposx
        return move__
    
    @staticmethod
    def is_possible_queenmove_classical(move__,board,justtest):
        if abs(move__.startposy-move__.endposy)==abs(move__.startposx-move__.endposx):
            return Rules.is_path_clear_bishop_classical(move__,board,justtest)
        if move__.startposy==move__.endposy or move__.startposx==move__.endposx:
            return Rules.is_path_clear_rook_classical(move__,board,justtest)
        return False

    @staticmethod
    def is_possible_kingmove_classical(move__,board,justtest):
        if abs(move__.startposy-move__.endposy)<=1 and abs(move__.startposx-move__.endposx)<=1:
            return move__
        print("check castle")
        #checking castle
        if not any(move__.piece==tup.piece for tup in board.move_list):
            if not Rules.checking_check(move__.piece.color,board): 
                if move__.piece.color=="white":
                    print("check white castle")
                    direction=1 if move__.startposx-move__.endposx<0 else -1
                    print(move__.piece.positiony,move__.piece.positionx)
                    if move__.piece.positiony==7 and move__.piece.positionx==4:
                        print("king on right position")
                        if abs(move__.startposx-move__.endposx)==2 and move__.endposy==move__.startposy:
                            if direction==1:
                                print("castle could be okay")
                                if isinstance(board.board[7][7],Rook):
                                    print("also a rook")
                                    if any(board.board[7][7]==tup.piece for tup in board.move_list):
                                        return False
                                    for j in range(1,3):
                                        if board.board[move__.endposy][move__.startposx+(direction*j)]!=None:
                                            return False
                                        for p in board.blackpieces:
                                            move_=ChessMove(p.positiony,p.positionx,move__.endposy,move__.startposx+(direction*j),p)
                                            if Rules.is_possible_move(move_,board,justtest=True):
                                                return False
                                    
                                    move__.castle_secondpiece=board.board[7][7]  
                                    move__.castle_secondpiece_posy=7     
                                    move__.castle_secondpiece_posx=7     
                                else:
                                    return False
                            elif direction==-1:
                                if isinstance(board.board[7][0],Rook):
                                    if any(board.board[7][0]==tup.piece for tup in board.move_list):
                                        return False
                                    for j in range(1,4):
                                        if board.board[move__.endposy][move__.startposx+(direction*j)]!=None:
                                            return False
                                        for p in board.blackpieces:
                                            move_=ChessMove(p.positiony,p.positionx,move__.endposy,move__.startposx+(direction*j),p)
                                            if Rules.is_possible_move(move_,board,justtest=True):
                                                return False
                                    
                                    move__.castle_secondpiece=board.board[7][0]
                                    move__.castle_secondpiece_posy=7  
                                    move__.castle_secondpiece_posx=0   
                                else:
                                    return False
                            print("its a castle")
                            move__.is_castle=True
                            return move__
                if move__.piece.color=="black":
                    direction=1 if move__.startposx-move__.endposx<0 else -1
                    if move__.piece.positiony==0 and move__.piece.positionx==4:
                        if abs(move__.startposx-move__.endposx)==2 and move__.endposy==move__.startposy:
                            if direction==1:
                                if isinstance(board.board[0][7],Rook):
                                    if any(board.board[0][7]==tup.piece for tup in board.move_list):
                                        return False
                                    for j in range(1,3):    
                                        if board.board[move__.endposy][move__.startposx+direction*j]!=None:
                                            return False
                                        for p in board.whitepieces:
                                            move_=ChessMove(p.positiony,p.positionx,move__.endposy,move__.startposx+(direction*j),p)
                                            if Rules.is_possible_move(move_,board,justtest=True):
                                                return False
                                    
                                    move__.castle_secondpiece=board.board[0][7] 
                                    move__.castle_secondpiece_posy=0
                                    move__.castle_secondpiece_posx=7
                                else:
                                    return False
                            elif direction==-1:
                                if isinstance(board.board[0][0],Rook):
                                    if any(board.board[0][0]==tup.piece for tup in board.move_list):
                                        return False
                                    for j in range(1,4):
                                        if board.board[move__.endposy][move__.startposx+direction*j]!=None:
                                            return False
                                        for p in board.whitepieces:
                                            move_=ChessMove(p.positiony,p.positionx,move__.endposy,move__.startposx+(direction*j),p)
                                            if Rules.is_possible_move(move_,board,justtest=True):
                                                return False
                                    
                                    move__.castle_secondpiece=board.board[0][0]
                                    move__.castle_secondpiece_posy=0  
                                    move__.castle_secondpiece_posx=0 
                                else: 
                                    return False
                            
                            move__.is_castle=True
                            return move__
        return False

    @staticmethod #if endsquare has an own piece on it
    def is_own_piece(move__,board):
        if board.board[move__.endposy][move__.endposx]!=None:
            if move__.piece.color==board.board[move__.endposy][move__.endposx].color:
                return True
            return False
        return False
    
    @staticmethod #if the given color is in check
    def checking_check(color,board):
        if board.ruleset_=="classical":
            # print("now checking check")
            king_positiony=board.piece_lookup["K",color][0].positiony
            king_positionx=board.piece_lookup["K",color][0].positionx
            if color=="white":
                for piece_ in board.blackpieces:
                    # print(piece_)
                    # print(piece_.position)
                    if not isinstance(piece_,King):
                        move_to_try=ChessMove(piece_.positiony,piece_.positionx,king_positiony,king_positionx,piece_)
                        if Rules.is_possible_move(move_to_try,board,justtest=True): #..
                            # print("check detected")
                            return True
                # print("no check detected")
                return False
            if color=="black":
                for piece_ in board.whitepieces:
                    move_to_try=ChessMove(piece_.positiony,piece_.positionx,king_positiony,king_positionx,piece_)
                    if Rules.is_possible_move(move_to_try,board,justtest=True):
                        return True
                return False
            # print("no check detected")
            return False
        
    
    @staticmethod #if the given color is in mate
    def checking_mate(color,board):
        # print(board.board[1][5])
        # print(board.blackpieces)
        # print(len(board.blackpieces))
        if board.ruleset_=="classical":
            if Rules.checking_check(color,board):
                if color=="white":
                    for piece in board.whitepieces:
                        for r in range(8):
                            for c in range(8):
                                move_=ChessMove(piece.positiony,piece.positionx,r,c,piece)
                                if Rules.is_valid_move(move_,board,justtest=True):
                                    return False
                    
                    return True
                if color=="black":
                    for piece in board.blackpieces:
                        # print(piece.position)
                        # print(board.board[1][5])
                        for r in range(8):
                            for c in range(8):
                                move_=ChessMove(piece.positiony,piece.positionx,r,c,piece)
                                if Rules.is_valid_move(move_,board,justtest=True):
                                    # print("no checkmate!")
                                    return False
                    # print("checkmate!")
                    return True
            else:
                return False
    
    @staticmethod #if move is possible, it does the move and checking for check and take the move back
    def testing_move(move__,board,promotion_choice,justtest=False):
        move__.promotion_choice=(Rook(move__.piece.color)) #just to check if there s a check after
        board.make_move(move__)
        if Rules.checking_check(move__.piece.color,board):
            board.take_move_back(move__)
            move__.promotion_choice=None
            return False
        else:
            board.take_move_back(move__)
            move__.promotion_choice=None
            if move__.is_promotion:
                if not justtest:
                    while move__.promotion_choice==None:
                        choice=promotion_choice(move__.piece.color)
                        if choice=="Queen":
                            move__.promotion_choice=((Queen(move__.piece.color)))
                        elif choice=="Rook":
                            move__.promotion_choice=((Rook(move__.piece.color)))
                        elif choice=="Bishop":
                            move__.promotion_choice=((Bishop(move__.piece.color)))
                        elif choice=="Knight":
                            move__.promotion_choice=((Knight(move__.piece.color)))
            return move__
    
    # @staticmethod
    # def extract_moves_from_informations(piece,startrow,startcol,endrow,endcol,ruleset,board,promotion_choice): 
    #     if ruleset=="classical":
    #         moves=[]
    #         #check castle
    #         if isinstance(piece,King):
    #             if abs(startcol-endcol)==2:
    #                 direction=1 if startcol-endcol<0 else -1
    #                 moves.append((piece,startrow,startcol,endrow,endcol))
    #                 if direction==1:
    #                     moves.append((board.board[startrow][7],startrow,7,endrow,endcol-1))
    #                 elif direction==-1:
    #                     moves.append((board.board[startrow][0],startrow,0,endrow,endcol+1))
    #                 return moves
    #         #check pawn on last row and en passant
    #         if isinstance(piece,Pawn):
    #             #check last row
    #             if endrow==0 or endrow==7:
    #                 moves.append((piece,startrow,startcol,None,None))
    #                 moves.append((board.board[endrow][endcol],endrow,endcol,None,None))
    #                 chosen_piece = None
    #                 while len(moves)==2:
    #                     chosen_piece = promotion_choice(piece.color)
    #                     if chosen_piece=="Queen":
    #                         moves.append((Queen(piece.color),None,None,endrow,endcol))
    #                     elif chosen_piece=="Rook":
    #                         moves.append((Rook(piece.color),None,None,endrow,endcol))
    #                     elif chosen_piece=="Bishop":
    #                         moves.append((Bishop(piece.color),None,None,endrow,endcol))
    #                     elif chosen_piece=="Knight":
    #                         moves.append((Knight(piece.color),None,None,endrow,endcol))
    #                 return moves
    #             #en passant
    #             if abs(startcol-endcol)==1 and board.board[endrow][endcol]==None:
    #                 moves.append((piece,startrow,startcol,endrow,endcol))
    #                 try:
    #                     moves.append((board.board[startrow][endcol],startrow,endcol,None,None))
    #                 except AttributeError:
    #                     pass
    #                 return moves
    #         return [(piece,startrow,startcol,endrow,endcol)]



            
