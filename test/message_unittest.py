__author__ = 'MCP'


import unittest
from lib.message import ClientMessageParser
from lib.message import ServerMessageParser


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


class ServerMessageParserTest(unittest.TestCase):

    def test_strinToArray(self):
        c = ServerMessageParser()
        s = "AB;CD;EF;GH"
        conversion = c.stringToArray(s)
        self.assertListEqual(conversion, ["AB", "CD", "EF", "GH"])


if __name__ == "__main__":
    unittest.main()