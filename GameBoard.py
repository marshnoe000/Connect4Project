from enum import Enum
from Player import Player
from Token import Token


# Notes: We could potentially implement the pop out version of Connect 4 if we need more stuff to do
def getStartingPlayer(player1, player2):
    return player1 if player1.goesFirst else player2

class GameBoard:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.grid = [[Token.EMPTY for _ in range(cols)] for _ in range(rows)]
        self.winningSequence = []

    def printBoard(self):
        for row in self.grid:
            print('| ' + ' | '.join(str(cell) for cell in row) + ' |')

        print('+---' * self.cols + '+')
        print('+' + '-'.join(
            ['{:^3}'.format(i) for i in range(self.cols)]) + '+')  # centers the col number in the col        

    def dropToken(self, col, token: Token):
        for row in range(self.rows - 1, -1, -1):
            if self.grid[row][col] == Token.EMPTY:
                self.grid[row][col] = token
                return True
        return False

    def removeToken(self, col):
        for row in range(self.rows - 1, -1, -1):
            if self.grid[row][col] != Token.EMPTY:
                self.grid[row][col] = Token.EMPTY
                return True
        return False

    def isValidMove(self, col):
        return 0 <= col < self.cols and self.grid[0][col] == Token.EMPTY

    def isFull(self):
        return all(self.isColumnFull(col) for col in range(self.cols))

    def isColumnFull(self, col):
        return self.grid[0][col] != Token.EMPTY

    def getValidMoves(self):
        validMoves = []
        for col in [3, 2, 4, 0, 1, 5, 6]:
            if not self.isColumnFull(col):
                validMoves.append(col)
        return validMoves

    def hasPlayerWon(self, player: Player):
        return self.checkHorizontal(player) or self.checkVertical(player) or self.checkDiagonals(player)

    def checkHorizontal(self, player: Player):
        for row in range(self.rows):
            for col in range(self.cols - 3):
                if (self.grid[row][col] == player.token and
                        self.grid[row][col + 1] == player.token and
                        self.grid[row][col + 2] == player.token and
                        self.grid[row][col + 3] == player.token):
                    self.winningSequence = [(row, col), (row, col + 1), (row, col + 2), (row, col + 3)]
                    return True
        return False

    def checkVertical(self, player: Player):
        for row in range(self.rows - 3):
            for col in range(self.cols):
                if (self.grid[row][col] == player.token and
                        self.grid[row + 1][col] == player.token and
                        self.grid[row + 2][col] == player.token and
                        self.grid[row + 3][col] == player.token):
                    self.winningSequence = [(row, col), (row + 1, col), (row + 2, col), (row + 3, col)]
                    return True
        return False

    def checkDiagonals(self, player: Player):
        # Check bottom-left to top-right
        for row in range(self.rows - 3):
            for col in range(self.cols - 3):
                if (self.grid[row][col] == player.token and
                        self.grid[row + 1][col + 1] == player.token and
                        self.grid[row + 2][col + 2] == player.token and
                        self.grid[row + 3][col + 3] == player.token):
                    return True

        # Check bottom-right to top-left
        for row in range(self.rows - 3):
            for col in range(3, self.cols):
                if (self.grid[row][col] == player.token and
                        self.grid[row + 1][col - 1] == player.token and
                        self.grid[row + 2][col - 2] == player.token and
                        self.grid[row + 3][col - 3] == player.token):
                    self.winningSequence = [(row, col), (row + 1, col - 1), (row + 2, col - 2), (row + 3, col - 3)]
                    return True

        return False

    def copy(self):
        copiedBoard = GameBoard(6,7)
        copiedBoard.grid = [row[:] for row in self.grid]
        return copiedBoard
