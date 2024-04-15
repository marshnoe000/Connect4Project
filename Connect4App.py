import time
import tkinter as tk

from AiAgent import AiAgent
from Token import Token
from GameBoard import GameBoard, getStartingPlayer
from Player import Player


class ConnectFourGUI:
    def __init__(self, master):
        self.current_player = None
        self.player1 = None
        self.player2 = None
        self.master = master
        self.master.title("Connect Four")
        self.game_board = None
        self.firstMove = True

        self.create_player_submission()

    def create_player_submission(self):
        # Create frame for player input and toggles
        self.player_frame = tk.Frame(self.master)
        self.player_frame.grid(row=0, column=0, sticky="nsew", padx=100, pady=(50, 15))

        # Configure row and column to expand and center player frame
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Player 1 input fields and toggles
        self.player1_label = tk.Label(self.player_frame, text="Player 1(Red):", font=("Comic Sans MS", 18))
        self.player1_label.grid(row=0, column=0, sticky="e", pady=(0, 2))
        self.player1_name_entry = tk.Entry(self.player_frame)
        self.player1_name_entry.grid(row=0, column=1, sticky="w", padx=(0, 10), pady=(0, 2))

        # Player 2 input fields and toggles
        self.player2_label = tk.Label(self.player_frame, text="Player 2(Yellow):", font=("Comic Sans MS", 18))
        self.player2_label.grid(row=1, column=0, sticky="e", pady=(0, 2))
        self.player2_name_entry = tk.Entry(self.player_frame)
        self.player2_name_entry.grid(row=1, column=1, sticky="w", padx=(0, 10), pady=(0, 2))

        # Submit button
        self.submit_button = tk.Button(self.player_frame, text="Submit", command=self.create_game_board,
                                       font=("Comic Sans MS", 18))
        self.submit_button.grid(row=2, columnspan=2, pady=(15, 0), sticky="n")

        # Configure row and column to expand and center player frame
        self.player_frame.grid_rowconfigure(0, weight=1)
        self.player_frame.grid_rowconfigure(1, weight=1)
        self.player_frame.grid_rowconfigure(2, weight=8)
        self.player_frame.grid_columnconfigure(0, weight=1)
        self.player_frame.grid_columnconfigure(1, weight=1)

    def create_game_board(self):
        # Retrieve player information
        player1_name = self.player1_name_entry.get()
        player2_name = self.player2_name_entry.get()

        # Create player objects
        if not player1_name:
            self.player1 = Player("Bot", Token.RED, True)
        else:
            self.player1 = Player(player1_name, Token.RED, False)

        if not player2_name:
            self.player2 = Player("Bot", Token.YELLOW, True)
        else:
            self.player2 = Player(player2_name, Token.YELLOW, False)

        # Create game board
        self.game_board = GameBoard()
        self.current_player = getStartingPlayer(self.player1, self.player2)

        # Destroy player input widgets
        self.player_frame.destroy()

        # Create game board widgets
        self.create_board_widgets()

    def create_board_widgets(self):
        # Create label for displaying player's turn
        self.turn_label = tk.Label(self.master, text="Player's Turn: " + self.current_player.name, bg="white",
                                   fg="black", font=("Comic Sans MS", 24))
        self.turn_label.grid(row=0, column=0, sticky="nsew")

        # Create canvas for game board
        self.canvas = tk.Canvas(self.master, bg="DodgerBlue3")
        self.canvas.grid(row=1, column=0, sticky="nsew")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)

        self.canvas.bind("<Configure>", self.on_canvas_resize)

        self.circles = []

        self.button_frame = tk.Frame(self.master)
        self.button_frame.grid(row=2, column=0, sticky="nsew")

        for col in range(7):
            button = tk.Button(self.button_frame, text=str(col), bg="white", fg="black", bd=0, font=("Helvetica", 14),
                               command=lambda c=col: self.drop_token(c))
            button.grid(row=0, column=col, sticky="nsew", padx=5)
            self.button_frame.columnconfigure(col, weight=5)
        if self.current_player.isBot and self.firstMove:
            self.firstMove = False
            bestMove = AiAgent.findBestMove(self.game_board, self.game_board.getValidMoves(), self.current_player)
            self.game_board.dropToken(bestMove, self.current_player.token)
            self.current_player = self.player2 if self.current_player is self.player1 else self.player1
            self.turn_label.config(text="Player's Turn: " + self.current_player.name, font=("Comic Sans MS", 24))

        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        cell_width = width / 7
        cell_height = height / 6

        winning_sequence = self.game_board.winningSequence  # Assuming winningSequence is a list of tuples

        for row in range(6):
            for col in range(7):
                x0 = col * cell_width + cell_width * 0.1
                y0 = row * cell_height + cell_height * 0.1
                x1 = (col + 1) * cell_width - cell_width * 0.1
                y1 = (row + 1) * cell_height - cell_height * 0.1
                color = self.game_board.grid[row][col]
                fill_color = "white"

                # Check if current token coordinates match any in the winning sequence
                if (row, col) in winning_sequence:
                    if self.current_player == self.player1:
                        fill_color = "firebrick3"
                    else:
                        fill_color = "gold"

                elif color is not Token.EMPTY:
                    fill_color = color.name

                circle = self.canvas.create_oval(x0, y0, x1, y1, fill=fill_color, outline="black")
                self.circles.append(circle)

    def on_canvas_resize(self, event):
        self.draw_board()

    def drop_token(self, col):
        if self.game_board.isValidMove(col) and not self.game_board.isFull():
            successful = self.game_board.dropToken(col, self.current_player.token)
            self.draw_board()
            if successful is True:
                if self.game_board.hasPlayerWon(self.current_player):
                    self.displayWin()
                    self.display_congratulations()
                else:
                    self.current_player = self.player2 if self.current_player == self.player1 else self.player1
                    self.turn_label.config(text="Player's Turn: " + self.current_player.name, font=("Comic Sans MS", 24))
                if self.current_player.isBot is True:
                    bestMove = AiAgent.findBestMove(self.game_board, self.game_board.getValidMoves(), self.current_player)
                    self.draw_board()
                    self.game_board.dropToken(bestMove, self.current_player.token)
                    self.draw_board()
                if self.game_board.hasPlayerWon(self.current_player):
                    self.displayWin()
                    self.display_congratulations()
                else:
                    self.current_player = self.player2 if self.current_player == self.player1 else self.player1
                    self.turn_label.config(text="Player's Turn: " + self.current_player.name, font=("Comic Sans MS", 24))



    def display_congratulations(self):
        # Create a new window to display congratulations message
        congrats_window = tk.Toplevel(self.master)
        congrats_window.title("Congratulations!")

        # Add label with congratulatory message
        congrats_label = tk.Label(congrats_window, text="Congratulations, " + self.current_player.name + "! You won!", font=("Comic Sans MS", 24))
        congrats_label.pack(pady=20)

        # Add exit button
        exit_button = tk.Button(congrats_window, text="Exit", command=self.exit_game)
        exit_button.pack(pady=10)

    def exit_game(self):
        self.master.destroy()

    def displayWin(self):
        self.draw_board()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x500")

    app = ConnectFourGUI(root)
    root.mainloop()
