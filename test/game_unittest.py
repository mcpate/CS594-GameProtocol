__author__ = 'MCP'


import unittest
from lib.game import Card
from lib.game import Deck


class CardTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

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

    def setUp(self):
        pass

    def tearDown(self):
        pass

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


if __name__ == "__main__":
    unittest.main()