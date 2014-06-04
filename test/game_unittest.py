__author__ = 'MCP'


import unittest
from lib.game import Card
from lib.game import Deck
from lib.game import Game
from lib.game import Player


class CardTest(unittest.TestCase):

    def test_returnsCorrectValue(self):
        card = Card('QH')
        self.assertEqual(card.value, 'QH')

    def test_returnsCorrectIntValue(self):
        card1 = Card("9C")
        card2 = Card("10H")
        card3 = Card("JD")
        card4 = Card("QC")
        card5 = Card("KD")
        card6 = Card("AS")
        self.assertEqual(card1.intValue(), 9)
        self.assertEqual(card2.intValue(), 10)
        self.assertEqual(card3.intValue(), 11)
        self.assertEqual(card4.intValue(), 12)
        self.assertEqual(card5.intValue(), 13)
        self.assertEqual(card6.intValue(), 14)


class DeckTest(unittest.TestCase):

    def test_hasCorrectNumCards(self):
        deck = Deck()
        self.assertEqual(len(deck.cards), 52)

    @unittest.skip('(skipping printout of shuffle)')
    def test_performsShuffle(self):
        deck = Deck()
        deck.cards = [Card("1A"), Card("2B"), Card("3C")]
        for card in deck.cards:
            print(card.value)
        deck.shuffle()
        for card in deck.cards:
            print(card.value)



class GameTest(unittest.TestCase):

    def setUp(self):
        self.m = Player('Matt', 'DummySocket')
        self.j = Player('Jamie', 'DummySocket')

    def test_dealCardsDealsCorrectly(self):
        deck = Deck()
        game = Game('SomeGameName', self.m)
        game.addPlayer(self.j)  # This isn't really necessary.
        game.dealCards([self.m, self.j], deck)
        self.assertEqual(self.m.hand.size(), 3)
        self.assertEqual(self.m.up.size(), 3)
        self.assertEqual(self.m.down.size(), 3)
        self.assertEqual(self.j.hand.size(), 3)
        self.assertEqual(self.j.up.size(), 3)
        self.assertEqual(self.m.down.size(), 3)
        self.assertEqual(deck.size(), (52 - 18))

    def test_returnsRotationOfPlayers(self):
        game = Game("SomeGame", self.m)
        game.addPlayer(self.j)
        game.beginGame()
        self.assertEqual(len(game.currentTurn), 1)
        self.assertRegex(game.currentPlayer.name, self.j.name)
        nextPlayer = game.getNextPlayer()
        self.assertRegex(nextPlayer.name, self.m.name)
        nextPlayer = game.getNextPlayer()
        self.assertRegex(nextPlayer.name, self.j.name)

    def test_rotatesPlayersCorrectly(self):
        game = Game("SomeGameName", self.m)
        game.addPlayer(self.j)
        game.beginGame()
        self.assertRegex(game.currentPlayer.name, self.j.name)
        game.rotateCurrentPlayer()
        self.assertRegex(game.currentPlayer.name, self.m.name)


if __name__ == "__main__":
    unittest.main()