from Token import Token
class Player:
    def __init__(self, name, token: Token, isBot):
        self.name = name
        self.goesFirst = True if token == Token.RED else False
        self.token = token
        self.isBot = isBot
