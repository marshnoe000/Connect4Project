from AiAgent import AiAgent
from GameBoard import GameBoard, getStartingPlayer
from Player import Player
from Token import Token

if __name__ == "__main__":
    board = GameBoard()
    player1 = Player("Noelle", Token.RED, False)
    player2 = Player("Kyle", Token.YELLOW, False)
    currentPlayer = getStartingPlayer(player1, player2)

    board.printBoard()
    stillPlaying = True
    while stillPlaying and not board.isFull():
        print(currentPlayer.name + "'s(" + currentPlayer.token.value + ") turn!")
        colNumber = int(input("Input column number:"))
        while board.isValidMove(colNumber) is False:
            colNumber = int(input("Input a different column number:"))

        board.dropToken(colNumber, currentPlayer.token)
        board.printBoard()
        bestMove = AiAgent.findBestMove(board, board.getValidMoves(), player2)
        print("Best Move: " + str(bestMove))

        if board.hasPlayerWon(player1):
            print("Congratulations " + player1.name + "! You won!")
            stillPlaying = False
        elif board.hasPlayerWon(player2):
            print("Congratulations" + player2.name + "! You won!")
            stillPlaying = False

        currentPlayer = player1 if currentPlayer == player2 else player2
