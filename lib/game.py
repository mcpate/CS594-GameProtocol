__author__ = 'MCP'


import random


class Game:

    def __init__(self):
        self.name = ""
        self.players = []
        self.deck = ["2C", "3C", "4C", "5C" "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC", "AC",
            "2D", "3D", "4D", "5D" "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD", "AD",
            "2S", "3S", "4S", "5S" "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS", "AS",
            "2H", "3H", "4H", "5H" "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH", "AH"]
        self.discard = []
        self.inProgress = False
        self.currentPlay = None

    def beginGame(self):
        self.inProgress = True
        self.shuffleDeck(self.deck)
        self.dealCards(self.players, self.deck, self.discard)

    def shuffleDeck(self, deck):
        deck = deck #todo: create shuffle

    # Assuming 2 players for now...
    def dealCards(self, to, deck, discard):
        player1 = to[0]
        player2 = to[1]
        #for _ in range(2):
        #    player1.faceDown.append(deck.pop)
        #    player2.faceDown.append(deck.pop)
        #for _ in range(2):
        #    player1.faceUp.append(deck.pop)
        #    player2.faceUp.append(deck.pop)
        for _ in range(3):
            player1.inHand.append(deck.pop())
            player2.inHand.append(deck.pop())
        #discard.append(deck.pop)

    def getOpponent(self, name):
        for player in self.players:
            if player.name != name:
                return player


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


class DiscardPile(Deck):

    def __init__(self):
        super().__init__()
        self.cards = []

    def add(self, card):
        assert isinstance(card, Card)
        self.cards.append(card)

    def clear(self):
        self.cards = []

    






class Player:

    def __init__(self, name, socket):
        #self.faceDown = []
        #self.faceUp = []
        self.inHand = []
        self.name = name
        self.socket = socket
        self.gameName = ""