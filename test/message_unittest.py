__author__ = 'MCP'


import unittest
from lib.message import ClientMessageParser


class ClientMessageParserTest(unittest.TestCase):

    def test_arrayToStringFormatsCorrectly(self):
        c = ClientMessageParser()
        a = ["one", "two", "three"]
        combined = c.arrayToString(a)
        self.assertRegex(combined, "three;two;one")

        a = ["one"]
        combined = c.arrayToString(a)
        self.assertRegex(combined, "one")

        a = []
        combined = c.arrayToString(a)
        self.assertEqual(combined, "")
        self.assertFalse(combined)


if __name__ == "__main__":
    unittest.main()