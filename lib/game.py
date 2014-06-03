__author__ = 'MCP'


import random


class Game:

    def __init__(self, name, creator):
        assert isinstance(creator, Player)
        self.name = name
        self.players = [creator]
        self.deck = Deck().shuffle()
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

    def getOpponent(self, name):
        for player in self.players:
            if player.name != name:
                return player

    def numPlayers(self):
        return len(self.players)


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
        self.cards = [Card("2C"), Card("3C"), Card("4C"), Card("5C"), Card("6C"), Card("7C"), Card("8C"), Card("9C"),
                      Card("10C"), Card("JC"), Card("QC"), Card("KC"), Card("AC"), Card("2D"), Card("3D"), Card("4D"),
                      Card("5D"), Card("6D"), Card("7D"), Card("8D"), Card("9D"), Card("10D"), Card("JD"), Card("QD"),
                      Card("KD"), Card("AD"), Card("2S"), Card("3S"), Card("4S"), Card("5S"), Card("6S"), Card("7S"),
                      Card("8S"), Card("9S"), Card("10S"), Card("JS"), Card("QS"), Card("KS"), Card("AS"), Card("2H"),
                      Card("3H"), Card("4H"), Card("5H"), Card("6H"), Card("7H"), Card("8H"), Card("9H"), Card("10H"),
                      Card("JH"), Card("QH"), Card("KH"), Card("AH")]

    def shuffle(self):
        random.shuffle(self.cards)

    def getCard(self):
        return self.cards.pop()

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
        self.hand = Pile()
        self.up = Pile()
        self.down = Pile()