import tkinter as tk
from chesspieces import *

class ChessGUI:
    def __init__(self,root,game):
        self.root=root
        self.topframe=tk.Frame(root)
        self.topframe.pack()
        self.bottomframe=tk.Frame(root)
        self.bottomframe.pack()

        #status label
        self.status_label = tk.Label(self.topframe, text=" ", font=("Arial", 14), bg="lightgray")
        self.status_label.pack(padx=10, pady=10)
        #label of current player
        self.current_player_label = tk.Label(self.topframe, text="white's turn", font=("Arial", 14), bg="lightgray")
        self.current_player_label.pack(padx=10, pady=10)
        self.board_frame = tk.Frame(self.topframe)
        self.board_frame.pack(padx=10, pady=10)
        self.create_gui_board(game)
        self.synchro_gui(game.chessboard_.board,game.chessgamedata.status,game.chessgamedata.current_player)
        self.restartbutton=tk.Button(self.bottomframe,
                                    bg="grey",
                                    padx=30,
                                    pady=10,
                                    font=('Arial', 16),
                                    command=lambda : game.restartgame())
        self.restartbutton.config(text="restart")
        # self.restartbutton.pack(padx=10, pady=10)
        self.restartbutton.grid(row=0 , column=0)
        self.lastgamebutton=tk.Button(self.bottomframe,
                                    bg="grey",
                                    padx=30,
                                    pady=10,
                                    font=('Arial', 16),
                                    command=lambda : game.lastgame())
        self.lastgamebutton.config(text="lastgame")
        # self.lastgamebutton.pack(padx=10, pady=10)
        self.lastgamebutton.grid(row=0 , column=1)
        self.nextgamebutton=tk.Button(self.bottomframe,
                                    bg="grey",
                                    padx=30,
                                    pady=10,
                                    font=('Arial', 16),
                                    command=lambda : game.nextgame())
        self.nextgamebutton.config(text="nextgame")
        # self.nextgamebutton.pack(padx=10, pady=10)
        self.nextgamebutton.grid(row=0 , column=2)
        self.lastmovebutton=tk.Button(self.bottomframe,
                                    bg="grey",
                                    padx=30,
                                    pady=10,
                                    font=('Arial', 16),
                                    command=lambda : game.lastmove())
        self.lastmovebutton.config(text="lastmove")
        self.lastmovebutton.grid(row=0 , column=3)
        self.nextmovebutton=tk.Button(self.bottomframe,
                                    bg="grey",
                                    padx=30,
                                    pady=10,
                                    font=('Arial', 16),
                                    command=lambda : game.nextmove())
        self.nextmovebutton.config(text="nextmove")
        self.nextmovebutton.grid(row=0 , column=4)
        # game.setup_gui_=self.setup_gui
        game.synchro_gui_=self.synchro_gui
        game.update_gui_=self.gui_update
        game.changes_gui_=self.gui_changes
        game.promotion_choice_=self.promotion_choice

    def create_gui_board(self,game):
        self.buttons=[[None for _ in range(8)] for _ in range(8)]
        for row in range(8):
            for col in range(8):
                color="light green" if (row+col)%2==0 else "green"
                button=tk.Button(self.board_frame,
                                    bg=color,
                                    padx=40,
                                    pady=40,
                                    font=('Arial', 24, 'bold'),
                                    command=lambda r=row, c=col: game.on_square_click(r,c))
                button.grid(row=row, column=col, sticky="nsew")
                self.buttons[row][col]=button
        for i in range(8):
            self.board_frame.grid_rowconfigure(i, weight=1, uniform="columns")
            self.board_frame.grid_columnconfigure(i, weight=1, uniform="rows")
    
    # def setup_gui(self,ruleset,status,current_player):  #replaced by synchro_gui
    #     self.current_player_label.config(text=f"{current_player}'s turn")
    #     self.status_label.config(text=status)
    #     if ruleset=="classical":
    #         self.setup_gui_classical()
    
    # def setup_gui_classical(self):
    #     whitepieces=["\u265C","\u265E","\u265D","\u265B","\u265A","\u265D","\u265E","\u265C"]
    #     blackpieces=["\u265C","\u265E","\u265D","\u265B","\u265A","\u265D","\u265E","\u265C"]
    #     for i in range(len(whitepieces)):
    #         self.buttons[7][i].config(text=whitepieces[i],fg="white")
    #         self.buttons[6][i].config(text="\u265F",fg="white")
    #         self.buttons[1][i].config(text="\u265F",fg="black")
    #         self.buttons[0][i].config(text=blackpieces[i],fg="black")
    #         self.buttons[2][i].config(text=" ")
    #         self.buttons[3][i].config(text=" ")
    #         self.buttons[4][i].config(text=" ")
    #         self.buttons[5][i].config(text=" ")

    def synchro_gui(self,board,status,current_player): #synchro the gui to the board
        self.current_player_label.config(text=f"{current_player}'s turn")
        self.status_label.config(text=status)
        for i in range(0,8):
            for j in range(0,8):
                p=board[i][j]
                if p:
                    text_=p.guisymbol
                    fg_=p.color
                else:
                    text_=" "
                    fg_=None
                self.buttons[i][j].config(text=text_,fg=fg_)

            

    def gui_update(self,currentplayer,status):#all gui changes after a move, the text data
        self.current_player_label.config(text=f"{currentplayer}'s turn")
        self.status_label.config(text=status)


    def gui_changes(self,row,col,element):#all gui changes for one square
        if element!=None:
            self.buttons[row][col].config(text=str(element),fg=element.color)
        else:
            self.buttons[row][col].config(text=" ")

    def promotion_choice(self,color): #gui function to select a piece for promotion
        self.gui_choice_= tk.StringVar()  

        self.top = tk.Toplevel(self.root)  
        self.top.title("pawn promotion")

        self.top.update_idletasks()  
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (self.top.winfo_reqwidth() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (self.top.winfo_reqheight() // 2)
        self.top.geometry(f"+{x}+{y}")  

        pieces_ = ["Queen", "Rook", "Bishop", "Knight"]
        symbols_ = ["♛", "♜", "♝", "♞"] if color == "white" else ["♕", "♖", "♗", "♘"]

        tk.Label(self.top, text="choose a piece:", font=("Arial", 14)).pack(pady=10)


        for piece, symbol in zip(pieces_, symbols_):
            btn = tk.Button(self.top, text=symbol, font=("Arial", 20),
                            command=lambda p=piece: self.set_piece(p))
            btn.pack(pady=5, padx=10, fill="x")

        self.top.wait_window()  
        return self.gui_choice_.get()


    def set_piece(self,piece): #part of promotion
        self.gui_choice_.set(piece)  
        self.top.destroy()  