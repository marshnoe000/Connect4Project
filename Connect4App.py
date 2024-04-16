import tkinter as tk

from AiAgent import AiAgent
from Token import Token
from GameBoard import GameBoard, getStartingPlayer
from Player import Player


# noinspection PyAttributeOutsideInit
# Adding fields to init function caused problems
class ConnectFourGUI:
    def __init__(self, master):
        self.current_player = None
        self.player1 = None
        self.player2 = None
        self.master = master
        self.master.title("Connect Four")
        self.gameBoard = None
        self.firstMove = True
        self.createPlayerSubmission()

    def createPlayerSubmission(self):
        self.playerFrame = tk.Frame(self.master)
        self.playerFrame.grid(row=0, column=0, sticky="nsew", padx=100, pady=(50, 15))

        # Expand and center player frame
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # Player 1 input fields and toggles
        self.player1Label = tk.Label(self.playerFrame, text="Player 1(Red):", font=("Comic Sans MS", 18))
        self.player1Label.grid(row=0, column=0, sticky="e", pady=(0, 2))
        self.player1NameEntry = tk.Entry(self.playerFrame)
        self.player1NameEntry.grid(row=0, column=1, sticky="w", padx=(0, 10), pady=(0, 2))

        # Player 2 input fields and toggles
        self.player2Label = tk.Label(self.playerFrame, text="Player 2(Yellow):", font=("Comic Sans MS", 18))
        self.player2Label.grid(row=1, column=0, sticky="e", pady=(0, 2))
        self.player2NameEntry = tk.Entry(self.playerFrame)
        self.player2NameEntry.grid(row=1, column=1, sticky="w", padx=(0, 10), pady=(0, 2))

        # Submit button
        self.submitButton = tk.Button(self.playerFrame, text="Submit", command=self.create_game_board,
                                      font=("Comic Sans MS", 18))
        self.submitButton.grid(row=2, columnspan=2, pady=(15, 0), sticky="n")

        # Configure weights for widget sizing
        self.playerFrame.grid_rowconfigure(0, weight=1)
        self.playerFrame.grid_rowconfigure(1, weight=1)
        self.playerFrame.grid_rowconfigure(2, weight=8)
        self.playerFrame.grid_columnconfigure(0, weight=1)
        self.playerFrame.grid_columnconfigure(1, weight=1)

    def create_game_board(self):
        # Retrieve player information
        self.createPlayers()

        self.gameBoard = GameBoard()
        self.currentPlayer = getStartingPlayer(self.player1, self.player2)

        # Destroy player selection screen
        self.playerFrame.destroy()

        self.createBoardWidgets()

    def createPlayers(self):
        player1_name = self.player1NameEntry.get()
        player2_name = self.player2NameEntry.get()
        if not player1_name:
            self.player1 = Player("Bot", Token.RED, True)
        else:
            self.player1 = Player(player1_name, Token.RED, False)
        if not player2_name:
            self.player2 = Player("Bot", Token.YELLOW, True)
        else:
            self.player2 = Player(player2_name, Token.YELLOW, False)

    def createBoardWidgets(self):
        self.createTurnLabel()

        # Create canvas for game board
        self.createGameBoard()
        if self.currentPlayer.isBot and self.firstMove:
            self.doBotsMove()

        self.drawBoard()

    def createTurnLabel(self):
        self.turnLabel = tk.Label(self.master, text="Player's Turn: " + self.currentPlayer.name, bg="white",
                                  fg="black", font=("Comic Sans MS", 24))
        self.turnLabel.grid(row=0, column=0, sticky="nsew")

    def doBotsMove(self):
        self.firstMove = False
        bestMove = AiAgent.findBestMove(self.gameBoard, self.gameBoard.getValidMoves(), self.currentPlayer)
        self.gameBoard.dropToken(bestMove, self.currentPlayer.token)
        self.currentPlayer = self.player2 if self.currentPlayer is self.player1 else self.player1
        self.turnLabel.config(text="Player's Turn: " + self.currentPlayer.name, font=("Comic Sans MS", 24))

    def createGameBoard(self):
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

    def drawBoard(self):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        cell_width = width / 7
        cell_height = height / 6

        winningSequence = self.gameBoard.tupleWinningSequence

        for row in range(6):
            for col in range(7):
                x0 = col * cell_width + cell_width * 0.1
                y0 = row * cell_height + cell_height * 0.1
                x1 = (col + 1) * cell_width - cell_width * 0.1
                y1 = (row + 1) * cell_height - cell_height * 0.1
                color = self.gameBoard.grid[row][col]
                fill_color = "white"

                # Check if current token coordinates match any in the winning sequence
                if (row, col) in winningSequence:
                    if self.currentPlayer == self.player1:
                        fill_color = "firebrick3"
                    else:
                        fill_color = "gold"

                elif color is not Token.EMPTY:
                    fill_color = color.name

                circle = self.canvas.create_oval(x0, y0, x1, y1, fill=fill_color, outline="black")
                self.circles.append(circle)

    def on_canvas_resize(self, event):
        self.drawBoard()

    def drop_token(self, col):
        if self.gameBoard.isValidMove(col) and not self.gameBoard.isFull():
            successful = self.gameBoard.dropToken(col, self.currentPlayer.token)
            self.drawBoard()
            if successful is True:
                self.checkWinOrSwapPlayer()
                if self.currentPlayer.isBot is True:
                    bestMove = AiAgent.findBestMove(self.gameBoard, self.gameBoard.getValidMoves(), self.currentPlayer)
                    self.drawBoard()
                    self.gameBoard.dropToken(bestMove, self.currentPlayer.token)
                    self.drawBoard()
                    self.checkWinOrSwapPlayer()

    def checkWinOrSwapPlayer(self):
        if self.gameBoard.hasPlayerWon(self.currentPlayer):
            self.displayWin()
            self.displayCongratulations()
        else:
            self.currentPlayer = self.player2 if self.currentPlayer == self.player1 else self.player1
            self.turnLabel.config(text="Player's Turn: " + self.currentPlayer.name, font=("Comic Sans MS", 24))

    def displayCongratulations(self):
        # Create a new window to display congratulations message
        congrats_window = tk.Toplevel(self.master)
        congrats_window.title("Congratulations!")

        # Add label with congratulations message
        congrats_label = tk.Label(congrats_window,
                                  text="Congratulations, " + self.currentPlayer.name + "! You won in " + str(
                                      self.gameBoard.totalTurns) + " turns!", font=("Comic Sans MS", 24))
        congrats_label.pack(pady=20)

        exit_button = tk.Button(congrats_window, text="Exit", command=self.exitGame)
        exit_button.pack(pady=10)

    def exitGame(self):
        self.master.destroy()

    def displayWin(self):
        self.drawBoard()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x500")

    app = ConnectFourGUI(root)
    root.mainloop()
