from database.base import Base
from chesspieces import *
from chessmove import *
#

class Rules: #just staticmethods
    def __init__(self,ruleset):
        pass

            
    @staticmethod #complete check of a move
    def is_valid_move(session,move__,gamedata,board,promotion_choice=None,justtest=False):
        move_=Rules.is_possible_move(session,move__,gamedata,board,justtest)
        if not move_:
            print("not possible")
            return False
        move_=Rules.testing_move(session,move_,gamedata,board,promotion_choice,justtest)
        if not move_:
            print("not testible")
            return False
    

        return move_
    
    @staticmethod #if the logic of the piece would allow the move
    def is_possible_move(session,move__,gamedata,board,justtest=False):
        if gamedata.ruleset_=="classical":
            if Rules.is_own_piece(move__,board) is True:
                print("is an own piece")
                return False
            if (move__.startposy,move__.startposx)==(move__.endposy,move__.endposx):
                print("not changed the position")
                return False
            if isinstance(move__.piece,Pawn):
                return Rules.is_possible_pawnmove_classical(session,move__,board,justtest)
            elif isinstance(move__.piece,Rook):
                return Rules.is_possible_rookmove_classical(move__,board,justtest)
            elif isinstance(move__.piece,Knight):
                return Rules.is_possible_knightmove_classical(move__,board,justtest)
            elif isinstance(move__.piece,Bishop):
                return Rules.is_possible_bishopmove_classical(move__,board,justtest)
            elif isinstance(move__.piece,Queen):
                return Rules.is_possible_queenmove_classical(move__,board,justtest)
            elif isinstance(move__.piece,King):
                return Rules.is_possible_kingmove_classical(session,move__,gamedata,board,justtest)

    @staticmethod
    def is_possible_pawnmove_classical(session,move__,board,justtest):
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
            and board.board[move__.startposy][move__.endposx].color!=move__.piece.color:
                last_move = session.query(ChessMove).filter_by(board_id=board.id).order_by(ChessMove.id.desc()).first()
                if last_move:
                    if last_move.endposy==move__.startposy\
                    and last_move.endposx==move__.endposx\
                    and last_move.startposx==move__.endposx\
                    and last_move.startposy==move__.endposy+direction:
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
    def is_possible_kingmove_classical(session,move__,gamedata,board,justtest):
        if abs(move__.startposy-move__.endposy)<=1 and abs(move__.startposx-move__.endposx)<=1:
            move__.captured_piece=board.board[move__.endposy][move__.endposx]
            move__.captured_piece_posy=move__.endposy
            move__.captured_piece_posx=move__.endposx
            return move__
        # print("checking castle")
        #checking castle

        if not Rules.checking_check(session,move__.piece.color,gamedata,board): 
            # print("check prevents castle")
            if move__.piece.color=="white":
                # print("checking white castle")
                direction=1 if move__.startposx-move__.endposx<0 else -1
                if move__.piece.positiony==7 and move__.piece.positionx==4:
                    if abs(move__.startposx-move__.endposx)==2 and move__.endposy==move__.startposy:
                        if direction==1:
                            if isinstance(board.board[7][7],Rook):
                                move_list = session.query(ChessMove).filter_by(board_id=board.id).all()
                                print("ÜÜÜ",len(move_list))
                                if any(move__.piece==tup.piece for tup in move_list):
                                    return False
                                if any(board.board[7][7]==tup.piece for tup in move_list):
                                    # print("smth already moved")
                                    return False
                                for j in range(1,3):
                                    if board.board[move__.endposy][move__.startposx+(direction*j)]!=None:
                                        return False
                                    for p in board.blackpieces:
                                        move_=ChessMove(board.id,p.positiony,p.positionx,move__.endposy,move__.startposx+(direction*j),p)
                                        if Rules.is_possible_move(session,move_,gamedata,board,justtest=True):
                                            return False
                                
                                move__.castle_secondpiece=board.board[7][7]  
                                move__.castle_secondpiece_posy=7     
                                move__.castle_secondpiece_posx=7     
                            else:
                                return False
                        elif direction==-1:
                            if isinstance(board.board[7][0],Rook):
                                move_list = session.query(ChessMove).filter_by(board_id=board.id).all()
                                if any(move__.piece==tup.piece for tup in move_list):
                                    return False
                                if any(board.board[7][0]==tup.piece for tup in move_list):
                                    return False
                                for j in range(1,4):
                                    if board.board[move__.endposy][move__.startposx+(direction*j)]!=None:
                                        return False
                                    for p in board.blackpieces:
                                        move_=lightChessMove(board.id,p.positiony,p.positionx,move__.endposy,move__.startposx+(direction*j),p)
                                        if Rules.is_possible_move(session,move_,gamedata,board,justtest=True):
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
                                move_list = session.query(ChessMove).filter_by(board_id=board.id).all()
                                if any(move__.piece==tup.piece for tup in move_list):
                                    return False
                                if any(board.board[0][7]==tup.piece for tup in move_list):
                                    return False
                                for j in range(1,3):    
                                    if board.board[move__.endposy][move__.startposx+direction*j]!=None:
                                        return False
                                    for p in board.whitepieces:
                                        move_=lightChessMove(board.id,p.positiony,p.positionx,move__.endposy,move__.startposx+(direction*j),p)
                                        if Rules.is_possible_move(session,move_,gamedata,board,justtest=True):
                                            return False
                                
                                move__.castle_secondpiece=board.board[0][7] 
                                move__.castle_secondpiece_posy=0
                                move__.castle_secondpiece_posx=7
                            else:
                                return False
                        elif direction==-1:
                            if isinstance(board.board[0][0],Rook):
                                if any(board.board[0][0]==tup.piece for tup in move_list):
                                    return False
                                move_list = session.query(ChessMove).filter_by(board_id=board.id).all()
                                if any(move__.piece==tup.piece for tup in move_list):
                                    return False
                                for j in range(1,4):
                                    if board.board[move__.endposy][move__.startposx+direction*j]!=None:
                                        return False
                                    for p in board.whitepieces:
                                        move_=lightChessMove(board.id,p.positiony,p.positionx,move__.endposy,move__.startposx+(direction*j),p)
                                        if Rules.is_possible_move(session,move_,gamedata,board,justtest=True):
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
    def checking_check(session,color,gamedata,board):
        if gamedata.ruleset_=="classical":
            king_positiony=board.piece_lookup[f"K_{color}"][0].positiony
            king_positionx=board.piece_lookup[f"K_{color}"][0].positionx
            if color=="white":
                for piece_ in board.blackpieces:
                    # print(piece_)
                    # print(piece_.position)
                    if not isinstance(piece_,King):
                        move_to_try=lightChessMove(board.id,piece_.positiony,piece_.positionx,king_positiony,king_positionx,piece_)
                        if Rules.is_possible_move(session,move_to_try,gamedata,board,justtest=True): #..
                            return True
                # print("no check detected")
                return False
            if color=="black":
                for piece_ in board.whitepieces:
                    move_to_try=lightChessMove(board.id,piece_.positiony,piece_.positionx,king_positiony,king_positionx,piece_)
                    if Rules.is_possible_move(session,move_to_try,gamedata,board,justtest=True):
                        return True
                return False
            return False
        
    
    @staticmethod #if the given color is in mate
    def checking_mate(session,color,gamedata,board):
        # print(board.board[1][5])
        # print(board.blackpieces)
        # print(len(board.blackpieces))
        if gamedata.ruleset_=="classical":
            print("checking mate")
            
        if color=="white":
            for piece in board.whitepieces:
                possible_squares=Rules.get_possible_squares(piece)
                for sq in possible_squares:
                    if 0<=sq[0]<=7 and 0<=sq[1]<=7:
                        move_=lightChessMove(board.id,piece.positiony,piece.positionx,sq[0],sq[1],piece)
                        # print("protectingmove",move_.piece.positiony,move_.piece.positionx,r,c)
                        # print("f7",board.board[1][5])
                        if Rules.is_valid_move(session,move_,gamedata,board,justtest=True):
                            # print("no checkmate!")
                            return False
                # for r in range(8):
                #     for c in range(8):
                #         move_=ChessMove(board.id,piece.positiony,piece.positionx,r,c,piece)
                #         if Rules.is_valid_move(session,move_,gamedata,board,justtest=True):
                #             return False
            
            return True
        if color=="black":
            for piece in board.blackpieces:
                # print(piece.position)
                # print(board.board[1][5])
                possible_squares=Rules.get_possible_squares(piece)
                for sq in possible_squares:
                    if 0<=sq[0]<=7 and 0<=sq[1]<=7:
                        move_=lightChessMove(board.id,piece.positiony,piece.positionx,sq[0],sq[1],piece)
                        # print("protectingmove",move_.piece.positiony,move_.piece.positionx,r,c)
                        # print("f7",board.board[1][5])
                        if Rules.is_valid_move(session,move_,gamedata,board,justtest=True):
                            # print("no checkmate!")
                            return False
                # for r in range(8):
                #     for c in range(8):
                #         move_=ChessMove(board.id,piece.positiony,piece.positionx,r,c,piece)
                #         # print("protectingmove",move_.piece.positiony,move_.piece.positionx,r,c)
                #         # print("f7",board.board[1][5])
                #         if Rules.is_valid_move(session,move_,gamedata,board,justtest=True):
                #             # print("no checkmate!")
                #             return False
                #         # else:
                #         #     print("f7",board.board[1][5])
            # print("checkmate!")
            return True
    
        return False
    
    @staticmethod #if move is possible, it does the move and checking for check and take the move back
    def testing_move(session,move__,gamedata,board,promotion_choice,justtest=False):
        move__.promotion_choice=(Rook(move__.piece.color)) #just to check if there s a check after
        print("testing..")
        # print("before making",move__.captured_piece)
        board.make_move(session,move__)
        # print("before takeback",move__.captured_piece)

        if Rules.checking_check(session,move__.piece.color,gamedata,board):
            board.take_move_back(session,move__)
            # print("after takeback",move__.captured_piece)
            move__.promotion_choice=None
            return False
        else:
            board.take_move_back(session,move__)
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
        
    def get_possible_squares(piece):
        if piece:
            direction=1 if piece.color=="black" else -1
            if piece.symbol=="P":
                return [(piece.positiony+direction,piece.positionx),
                        (piece.positiony+2*direction,piece.positionx),
                        (piece.positiony+direction,piece.positionx+1),
                        (piece.positiony+direction,piece.positionx-1)]
            if piece.symbol=="K":
                return[(piece.positiony+1,piece.positionx),
                       (piece.positiony+1,piece.positionx+1),
                       (piece.positiony+1,piece.positionx-1),
                       (piece.positiony,piece.positionx+1),
                       (piece.positiony,piece.positionx-1),
                       (piece.positiony-1,piece.positionx),
                       (piece.positiony-1,piece.positionx+1),
                       (piece.positiony-1,piece.positionx-1),
                       (piece.positiony,piece.positionx+2),
                       (piece.positiony,piece.positionx-2)]
            if piece.symbol=="R":
                return[(piece.positiony,0),
                       (piece.positiony,1),
                       (piece.positiony,2),
                       (piece.positiony,3),
                       (piece.positiony,4),
                       (piece.positiony,5),
                       (piece.positiony,6),
                       (piece.positiony,7),
                       (0,piece.positionx),
                       (1,piece.positionx),
                       (2,piece.positionx),
                       (3,piece.positionx),
                       (4,piece.positionx),
                       (5,piece.positionx),
                       (6,piece.positionx),
                       (7,piece.positionx)]
            if piece.symbol=="N":
                return[(piece.positiony+2,piece.positionx+1),
                       (piece.positiony+2,piece.positionx-1),
                       (piece.positiony+1,piece.positionx+2),
                       (piece.positiony+1,piece.positionx-2),
                       (piece.positiony-1,piece.positionx+2),
                       (piece.positiony-1,piece.positionx-2),
                       (piece.positiony-2,piece.positionx+1),
                       (piece.positiony-2,piece.positionx+1)]
            if piece.symbol=="B":
                return[(piece.positiony+1,piece.positionx+1),
                       (piece.positiony+1,piece.positionx-1),
                       (piece.positiony+2,piece.positionx+2),
                       (piece.positiony+2,piece.positionx-2),
                       (piece.positiony+3,piece.positionx+3),
                       (piece.positiony+3,piece.positionx-3),
                       (piece.positiony+4,piece.positionx+4),
                       (piece.positiony+4,piece.positionx-4),
                       (piece.positiony+5,piece.positionx+5),
                       (piece.positiony+5,piece.positionx-5),
                       (piece.positiony+6,piece.positionx+6),
                       (piece.positiony+6,piece.positionx-6),
                       (piece.positiony+7,piece.positionx+7),
                       (piece.positiony+7,piece.positionx-7),
                       (piece.positiony-1,piece.positionx+1),
                       (piece.positiony-1,piece.positionx-1),
                       (piece.positiony-2,piece.positionx+2),
                       (piece.positiony-2,piece.positionx-2),
                       (piece.positiony-3,piece.positionx+3),
                       (piece.positiony-3,piece.positionx-3),
                       (piece.positiony-4,piece.positionx+4),
                       (piece.positiony-4,piece.positionx-4),
                       (piece.positiony-5,piece.positionx+5),
                       (piece.positiony-5,piece.positionx-5),
                       (piece.positiony-6,piece.positionx+6),
                       (piece.positiony-6,piece.positionx-6),
                       (piece.positiony-7,piece.positionx+7),
                       (piece.positiony-7,piece.positionx-7)
                       ]
            if piece.symbol=="Q":
                return [(piece.positiony+1,piece.positionx+1),
                       (piece.positiony+1,piece.positionx-1),
                       (piece.positiony+2,piece.positionx+2),
                       (piece.positiony+2,piece.positionx-2),
                       (piece.positiony+3,piece.positionx+3),
                       (piece.positiony+3,piece.positionx-3),
                       (piece.positiony+4,piece.positionx+4),
                       (piece.positiony+4,piece.positionx-4),
                       (piece.positiony+5,piece.positionx+5),
                       (piece.positiony+5,piece.positionx-5),
                       (piece.positiony+6,piece.positionx+6),
                       (piece.positiony+6,piece.positionx-6),
                       (piece.positiony+7,piece.positionx+7),
                       (piece.positiony+7,piece.positionx-7),
                       (piece.positiony-1,piece.positionx+1),
                       (piece.positiony-1,piece.positionx-1),
                       (piece.positiony-2,piece.positionx+2),
                       (piece.positiony-2,piece.positionx-2),
                       (piece.positiony-3,piece.positionx+3),
                       (piece.positiony-3,piece.positionx-3),
                       (piece.positiony-4,piece.positionx+4),
                       (piece.positiony-4,piece.positionx-4),
                       (piece.positiony-5,piece.positionx+5),
                       (piece.positiony-5,piece.positionx-5),
                       (piece.positiony-6,piece.positionx+6),
                       (piece.positiony-6,piece.positionx-6),
                       (piece.positiony-7,piece.positionx+7),
                       (piece.positiony-7,piece.positionx-7),
                       (piece.positiony,0),
                       (piece.positiony,1),
                       (piece.positiony,2),
                       (piece.positiony,3),
                       (piece.positiony,4),
                       (piece.positiony,5),
                       (piece.positiony,6),
                       (piece.positiony,7),
                       (0,piece.positionx),
                       (1,piece.positionx),
                       (2,piece.positionx),
                       (3,piece.positionx),
                       (4,piece.positionx),
                       (5,piece.positionx),
                       (6,piece.positionx),
                       (7,piece.positionx)
                       ]
            

    
    