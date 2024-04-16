from Token import Token
from GameBoard import GameBoard
from Player import Player

nextMove = None  # Define global variables outside
bestGameState = None
bestGameStateScore = 0

class AiAgent:
    @staticmethod
    def findBestMove(gameState: GameBoard, validMoves, player: Player):
        global nextMove
        global bestGameState
        global bestGameStateScore
        nextMove = 0
        turnMultiplier = 1 if player.goesFirst else -1
        AiAgent.negamaxWithAlphaBeta(gameState, validMoves, 5, turnMultiplier, 5,
                                     player.token)
        return nextMove

    @staticmethod
    def negamaxWithAlphaBeta(gameState: GameBoard, validMoves, depth, turnMultiplier, maxDepth, playerToken,
                             alpha=float('-inf'), beta=float('inf')):
        global nextMove
        global bestGameState
        global bestGameStateScore
        if depth == 0 or gameState.isFull():
            return AiAgent.scoreBoard(gameState, playerToken)

        maxScore = float('-inf')
        for move in validMoves:
            # Create a copy of the game state before making any modifications
            copiedGameState = gameState.copy()
            copiedGameState.dropToken(move, playerToken)
            nextMoves = copiedGameState.getValidMoves()
            newPlayerToken = Token.YELLOW if playerToken == Token.RED else Token.RED
            score = -AiAgent.negamaxWithAlphaBeta(copiedGameState, nextMoves, depth - 1, -turnMultiplier, maxDepth,
                                                  newPlayerToken, -beta, -alpha)
            # No need to remove the token since we're operating on a copied game state
            if score > maxScore:
                maxScore = score
                if depth == maxDepth:
                    bestGameStateScore = maxScore
                    nextMove = move
                    bestGameState = copiedGameState
            alpha = max(alpha, score)
            if alpha >= beta:
                break

        return maxScore

    @staticmethod
    def scoreBoard(gameBoard, playerToken):
        score = 0
        rowCount = 6
        colCount = 7
        groupCount = 4
        grid = gameBoard.grid

        centerArray = [row[colCount // 2] for row in grid]
        centerCount = centerArray.count(playerToken)
        score += centerCount * 3

        # Vertical
        for col in range(colCount):
            colArray = [grid[row][col] for row in range(rowCount)]
            for row in range(rowCount - groupCount + 1):
                group = colArray[row: row + groupCount]
                score += AiAgent.evaluateGrouping(group, playerToken)

        # Horizontal
        for row in range(rowCount):
            rowArray = [grid[row][col] for col in range(colCount)]
            for col in range(colCount - groupCount + 1):
                group = rowArray[col: col + groupCount]
                score += AiAgent.evaluateGrouping(group, playerToken)

        # Diagonal (bottom left to top right)
        for row in range(rowCount - groupCount + 1):
            for col in range(colCount - groupCount + 1):
                group = [grid[row + i][col + i] for i in range(groupCount)]
                score += AiAgent.evaluateGrouping(group, playerToken)

        # Diagonal (top left to bottom right)
        for row in range(groupCount - 1, rowCount):
            for col in range(colCount - groupCount + 1):
                group = [grid[row - i][col + i] for i in range(groupCount)]
                score += AiAgent.evaluateGrouping(group, playerToken)

        return score

    @staticmethod
    def evaluateGrouping(group, playerToken):
        score = 0

        oppToken = Token.YELLOW if playerToken is Token.RED else Token.RED

        if group.count(playerToken) == 4:
            score += 100
        elif group.count(playerToken) == 3 and group.count(Token.EMPTY) == 1:
            score += 5
        elif group.count(playerToken) == 2 and group.count(Token.EMPTY) == 2:
            score += 2

        if group.count(oppToken) == 3 and group.count(Token.EMPTY) == 1:
            score -= 15
        elif group.count(oppToken) == 4:
            score -= 100

        return score
