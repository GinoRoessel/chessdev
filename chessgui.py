import tkinter as tk
from chesspieces import *

class ChessGUI:
    def __init__(self,root,game):
        self.root=root
        #status label
        self.status_label = tk.Label(self.root, text=" ", font=("Arial", 14), bg="lightgray")
        self.status_label.pack(padx=10, pady=10)
        #label of current player
        self.current_player_label = tk.Label(self.root, text="white's turn", font=("Arial", 14), bg="lightgray")
        self.current_player_label.pack(padx=10, pady=10)
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(padx=10, pady=10)
        self.create_gui_board(game)

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
            self.board_frame.grid_rowconfigure(i, weight=1)
            self.board_frame.grid_columnconfigure(i, weight=1)
    
    def setup_gui(self,ruleset):
        if ruleset=="classical":
            self.setup_gui_classical()
    
    def setup_gui_classical(self):
        whitepieces=["\u265C","\u265E","\u265D","\u265B","\u265A","\u265D","\u265E","\u265C"]
        blackpieces=["\u265C","\u265E","\u265D","\u265B","\u265A","\u265D","\u265E","\u265C"]
        for i in range(len(whitepieces)):
            self.buttons[7][i].config(text=whitepieces[i],fg="white")
            self.buttons[6][i].config(text="\u265F",fg="white")
            self.buttons[1][i].config(text="\u265F",fg="black")
            self.buttons[0][i].config(text=blackpieces[i],fg="black")

    def gui_update(self,startrow,startcol,endrow,endcol,board,currentplayer,status):#all gui changes after a move
        self.gui_changes(startrow,startcol,board.board[startrow][startcol])
        self.gui_changes(endrow,endcol,board.board[endrow][endcol])
        self.current_player_label.config(text=f"{currentplayer}'s turn")
        self.status_label.config(text=status)


    def gui_changes(self,row,col,element):#all gui changes for one square
        if element!=None:
            self.buttons[row][col].config(text=str(element),fg=element.color)
        else:
            self.buttons[row][col].config(text=" ")