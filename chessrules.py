from chesspieces import *


class Rules: #just staticmethods
    def __init__(self,ruleset):
        pass

            
    @staticmethod #complete check of a move
    def is_valid_move(piece,startrow,startcol,endrow,endcol,ruleset,board):
        if not Rules.is_possible_move(piece,startrow,startcol,endrow,endcol,ruleset,board):
            print("not possible")
            return False
        print("is_valid_move: Rufe testing_move auf")
        if not Rules.testing_move(piece,startrow,startcol,endrow,endcol,ruleset,board):
            print("not working after test")
            return False
        # print("valid")
        return True
    
    @staticmethod #if the logic of the piece would allow the move
    def is_possible_move(piece,startrow,startcol,endrow,endcol,ruleset,board):
        if ruleset=="classical":
            if Rules.is_own_piece(piece,startrow,startcol,endrow,endcol,ruleset,board) is True:
                print("is an own piece")
                return False
            if (startrow,startcol)==(endrow,endcol):
                print("not changed the position")
                return False
            if isinstance(piece,Pawn):
                return Rules.is_possible_pawnmove_classical(piece,startrow,startcol,endrow,endcol,ruleset,board)
            if isinstance(piece,Rook):
                return Rules.is_possible_rookmove_classical(piece,startrow,startcol,endrow,endcol,ruleset,board)
            if isinstance(piece,Knight):
                return Rules.is_possible_knightmove_classical(piece,startrow,startcol,endrow,endcol,ruleset,board)
            if isinstance(piece,Bishop):
                return Rules.is_possible_bishopmove_classical(piece,startrow,startcol,endrow,endcol,ruleset,board)
            if isinstance(piece,Queen):
                return Rules.is_possible_queenmove_classical(piece,startrow,startcol,endrow,endcol,ruleset,board)
            if isinstance(piece,King):
                return Rules.is_possible_kingmove_classical(piece,startrow,startcol,endrow,endcol,ruleset,board)

    @staticmethod
    def is_possible_pawnmove_classical(piece,startrow,startcol,endrow,endcol,ruleset,board):
        # print("piece is",piece)
        # print("startrow is",startrow)
        # print("startcol is",startcol)
        # print("endrow is",endrow)
        # print("endcol is",endcol)
        direction=-1 if piece.color=="white" else 1
        if startcol==endcol: #geradeaus
            if endrow-startrow==direction and board.board[endrow][endcol] is None: #ein Feld
                return True
            if endrow-startrow==2*direction and startrow==(6 if piece.color == "white" else 1)\
                and board.board[endrow][endcol] is None and board.board[(endrow+startrow)//2][endcol] is None: #zwei Felder
                return True
        try: 
            if (startcol+1==endcol or startcol-1==endcol) and endrow-startrow==direction\
              and board.board[endrow][endcol].color!=piece.color: #diagonal schlagen
                return True
        except AttributeError:
            pass
        return False
            

    @staticmethod
    def is_possible_rookmove_classical(piece,startrow,startcol,endrow,endcol,ruleset,board):
        if startrow==endrow or startcol==endcol:
            return Rules.is_path_clear_rook_classical(piece,startrow,startcol,endrow,endcol,ruleset,board)
        else:
            return False

    def is_path_clear_rook_classical(piece,startrow,startcol,endrow,endcol,ruleset,board):
        if startrow==endrow:
            direction=1 if startcol<endcol else -1
            if abs(endcol-startcol)==1:
                return True
            for i in range(1,abs(endcol-startcol)):
                if board.board[startrow][startcol+(i*direction)] is not None:
                    return False
            return True  
        if startcol==endcol:
            direction=1 if startrow<endrow else -1
            if abs(endrow-startrow)==1:
                return True
            for i in range(1,abs(endrow-startrow)):
                if board.board[startrow+(i*direction)][startcol] is not None:
                    return False
            return True      
        return False

    @staticmethod
    def is_possible_knightmove_classical(piece,startrow,startcol,endrow,endcol,ruleset,board):
        if (abs(startrow-endrow)==2 or abs(startrow-endrow)==1) and \
        (abs(startcol-endcol)==2 or abs(startcol-endcol)==1) and \
        (abs(startrow-endrow)+abs(startcol-endcol)==3):
            return True
        else:
            return False

    @staticmethod
    def is_possible_bishopmove_classical(piece,startrow,startcol,endrow,endcol,ruleset,board):
        if abs(startrow-endrow)==abs(startcol-endcol):
            return Rules.is_path_clear_bishop_classical(piece,startrow,startcol,endrow,endcol,ruleset,board)
        else: 
            return False
        
    def is_path_clear_bishop_classical(piece,startrow,startcol,endrow,endcol,ruleset,board):
        if startrow>endrow and startcol>endcol:
            direction=(-1,-1)
        elif startrow>endrow and startcol<endcol:
            direction=(-1,1)
        elif startrow<endrow and startcol>endcol:
            direction=(1,-1)
        elif startrow<endrow and startcol<endcol:
            direction=(1,1)
        for i in range(1,abs(startrow-endrow)):
            if board.board[startrow+(direction[0]*i)][startcol+(direction[1]*i)] is not None:
                return False
        return True
    
    @staticmethod
    def is_possible_queenmove_classical(piece,startrow,startcol,endrow,endcol,ruleset,board):
        if abs(startrow-endrow)==abs(startcol-endcol):
            return Rules.is_path_clear_bishop_classical(piece,startrow,startcol,endrow,endcol,ruleset,board)
        if startrow==endrow or startcol==endcol:
            return Rules.is_path_clear_rook_classical(piece,startrow,startcol,endrow,endcol,ruleset,board)
        return False

    @staticmethod
    def is_possible_kingmove_classical(piece,startrow,startcol,endrow,endcol,ruleset,board):
        if abs(startrow-endrow)<=1 and abs(startcol-endcol)<=1:
            return True
        #checking castle
        if piece.color=="white":
            direction=1 if startcol-endcol<0 else -1
            if piece.position==(7,4):
                if abs(startcol-endcol)==2 and startrow==endrow:
                    if direction==1:
                        if isinstance(board.board[7][7],Rook):
                            for j in range(1,3):
                                if board.board[startrow][startcol+(direction*j)]!=None:
                                    return False
                    elif direction==-1:
                        if isinstance(board.board[7][0],Rook):
                            for j in range(1,4):
                                if board.board[startrow][startcol+(direction*j)]!=None:
                                    return False
                    return True
        if piece.color=="black":
            direction=1 if startcol-endcol>1 else -1
            if piece.position==(0,4):
                if abs(startcol-endcol)==2 and startrow==endrow:
                    if direction==1:
                        if isinstance(board.board[0][7],Rook):
                            for j in range(1,3):
                                if board.board[startrow][startrow+direction*j]!=None:
                                    return False
                    elif direction==-1:
                        if isinstance(board.board[0][0],Rook):
                            for j in range(1,4):
                                if board.board[startrow][startrow+direction*j]!=None:
                                    return False
                    return True


            
        return False

    @staticmethod #if endsquare has an own piece on it
    def is_own_piece(piece,startrow,startcol,endrow,endcol,ruleset,board):
        if board.board[endrow][endcol]!=None:
            if piece.color==board.board[endrow][endcol].color:
                return True
            return False
        return False
    
    @staticmethod #if the given color is in check
    def checking_check(board,color,ruleset):
        if ruleset=="classical":
            # print("now checking check")
            king_position=board.piece_lookup["K",color].position
            # print(king_position)
            if color=="white":
                for piece_ in board.blackpieces:
                    # print(piece_)
                    # print(piece_.position)
                    if Rules.is_possible_move(piece_,piece_.position[0],piece_.position[1],
                                              king_position[0],king_position[1],ruleset,board):
                        # print("check detected")
                        return True
                # print("no check detected")
                return False
            if color=="black":
                for piece in board.whitepieces:
                    if Rules.is_possible_move(piece,piece.position[0],piece.position[1],
                                              king_position[0],king_position[1],ruleset,board):
                        return True
                return False
            # print("no check detected")
            return False
        
    
    @staticmethod #if the given color is in mate
    def checking_mate(board,color,ruleset):
        print("checking the mate...")
        # print(board.board[1][5])
        # print(board.blackpieces)
        # print(len(board.blackpieces))
        if ruleset=="classical":
            if Rules.checking_check(board,color,ruleset):
                if color=="white":
                    for piece in board.whitepieces:
                        for r in range(8):
                            for c in range(8):
                                if Rules.is_valid_move(piece,piece.position[0],piece.position[1],r,c,ruleset,board):
                                    print("there is a move")
                                    return False
                    print("checkmate!")
                    
                    return True
                if color=="black":
                    for piece in board.blackpieces:
                        # print(piece.position)
                        # print(board.board[1][5])
                        for r in range(8):
                            for c in range(8):
                                if Rules.is_valid_move(piece,piece.position[0],piece.position[1],r,c,ruleset,board):
                                    print("no checkmate!")
                                    return False
                    print("checkmate!")
                    return True
            else:
                return False
    
    @staticmethod #if move is possible, it does the move and checking for check and take the move back
    def testing_move(piece,startrow,startcol,endrow,endcol,ruleset,board):
        board.update_board(piece,startrow,startcol,endrow,endcol)
        if Rules.checking_check(board,piece.color,ruleset):
            board.deupdate_board(piece,startrow,startcol,endrow,endcol)
            return False
        else:
            board.deupdate_board(piece,startrow,startcol,endrow,endcol)
            print("testing finished")
            return True
    
    @staticmethod
    def extract_moves_from_informations(piece,startrow,startcol,endrow,endcol,ruleset,board): 
        if ruleset=="classical":
            moves=[]
            #check castle
            if isinstance(piece,King):
                if abs(startcol-endcol)==2:
                    direction=1 if startcol-endcol<0 else -1
                    moves.append((piece,startrow,startcol,endrow,endcol))
                    if direction==1:
                        moves.append((board.board[startrow][7],startrow,7,endrow,endcol-1))
                    elif direction==-1:
                        moves.append((board.board[startrow][0],startrow,0,endrow,endcol+1))
                    return moves
            #check pawn on last row and en passant
            if isinstance(piece,Pawn):
                #check last row
                if endrow==0 or endrow==7:
                    moves.append((piece,startrow,startcol,None,None))
                    moves.append((board.board[endrow][endcol],endrow,endcol,None,None))
                    moves.append((Queen(piece.color),None,None,endrow,endcol))
                    return moves
            return [(piece,startrow,startcol,endrow,endcol)]



            
