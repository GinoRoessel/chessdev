class ChessMove():
    def __init__(self,startpos,endpos,piece,captured_piece=None,captured_piece_pos=None,is_enpassant=False,
                 is_castle=False,is_promotion=False,promotion_choice=None,
                 castle_secondpiece=None,castle_secondpiece_pos=None):
        self.startpos=startpos
        self.endpos=endpos
        self.piece=piece
        self.captured_piece=captured_piece
        self.captured_piece_pos=captured_piece_pos
        self.is_enpassant=is_enpassant
        self.is_castle=is_castle
        self.is_promotion=is_promotion
        self.promotion_choice=promotion_choice
        self.castle_secondpiece=castle_secondpiece
        self.castle_secondpiece_pos=castle_secondpiece_pos