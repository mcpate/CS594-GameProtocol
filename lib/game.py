__author__ = 'MCP'


import random


class Game:

    def __init__(self, name, creator):
        assert isinstance(creator, Player)
        self.name = name
        self.players = [creator]
        self.currentPlayer = None
        # Array of active player in 'this' turn.
        self.currentTurn = []
        self.deck = Deck()
        self.deck.shuffle()
        self.discard = Pile()
        self.inProgress = False

    def addPlayer(self, player):
        assert isinstance(player, Player)
        assert len(self.players) < 2
        self.players.append(player)

    def beginGame(self):
        assert len(self.players) == 2
        self.inProgress = True
        self.dealCards(self.players, self.deck)
        self.currentPlayer = self.getNextPlayer()

    def dealCards(self, players, deck):
        for _ in range(3):
            for player in players:
                player.down.addCard(deck.getCard())
        for _ in range(3):
            for player in players:
                player.up.addCard(deck.getCard())
        for _ in range(3):
            for player in players:
                player.hand.addCard(deck.getCard())

    def getNextPlayer(self):
        #for player in self.players:
        #    if self.currentPlayer is None or player.name != self.currentPlayer.name:
        #        return player
        # This should work for arbitrary number of players
        if len(self.currentTurn) == 0:
            for player in self.players:
                self.currentTurn.append(player)
            return self.currentTurn.pop()
        else:
            return self.currentTurn.pop()

    def getOpponent(self, player):
        assert isinstance(player, Player)
        for p in self.players:
            if p.name != player.name:
                return p

    def numPlayers(self):
        return len(self.players)

    def peekTopOfDiscard(self):
        if self.discard.size == 0:
            return "ERROR"
        else:
            return self.discard[0].value

    def rotateCurrentPlayer(self):
        self.currentPlayer = self.getNextPlayer()


class Card:

    def __init__(self, value):
        self.value = value

    def compare(self, value):
        assert isinstance(value, Card)
        if self.intValue() > value.intValue():
            return 1
        elif self.intValue() == value.intValue():
            return 0
        else:
            return -1

    def intValue(self):
        if self.value[0] == 'J':
            return 11
        elif self.value[0] == 'Q':
            return 12
        elif self.value[0] == 'K':
            return 13
        elif self.value[0] == 'A':
            return 14
        else:
            return int(self.value[0:-1])


class Deck:

    def __init__(self):
        #self.cards = [Card("2C"), Card("3C"), Card("4C"), Card("5C"), Card("6C"), Card("7C"), Card("8C"), Card("9C"),
        #              Card("10C"), Card("JC"), Card("QC"), Card("KC"), Card("AC"), Card("2D"), Card("3D"), Card("4D"),
        #              Card("5D"), Card("6D"), Card("7D"), Card("8D"), Card("9D"), Card("10D"), Card("JD"), Card("QD"),
        #              Card("KD"), Card("AD"), Card("2S"), Card("3S"), Card("4S"), Card("5S"), Card("6S"), Card("7S"),
        #              Card("8S"), Card("9S"), Card("10S"), Card("JS"), Card("QS"), Card("KS"), Card("AS"), Card("2H"),
        #              Card("3H"), Card("4H"), Card("5H"), Card("6H"), Card("7H"), Card("8H"), Card("9H"), Card("10H"),
        #              Card("JH"), Card("QH"), Card("KH"), Card("AH")]
        self.cards = [Card("2C"), Card("3C"), Card("4C"), Card("5C"), Card("6C"), Card("7C"), Card("8C"), Card("9C"),
                      Card("10C"), Card("JC"), Card("QC"), Card("KC"), Card("AC"), Card("2D"), Card("3D"), Card("4D"),
                      Card("5D"), Card("6D"), Card("7D"), Card("8D")]

    def shuffle(self):
        random.shuffle(self.cards)

    def getCard(self):
        if self.size() == 0:
            return None
        return self.cards.pop()

    def toStringArray(self):
        deck = []
        for card in self.cards:
            deck.append(card.value)
        return deck

    def removeByValue(self, value):
        for card in self.cards:
            if card.value == value:
                self.cards.remove(card)

    def size(self):
        return len(self.cards)


class Pile(Deck):

    def __init__(self):
        super().__init__()
        self.cards = []

    def addCard(self, card):
        assert isinstance(card, Card)
        self.cards.append(card)

    def clear(self):
        self.cards = []


class Player:

    def __init__(self, name, socket):
        self.name = name
        self.socket = socket
        self.game = None
        self.currentPlay = None
        self.hand = Pile()
        self.up = Pile()
        self.down = Pile()