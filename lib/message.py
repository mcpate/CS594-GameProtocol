__author__ = 'MCP'


class ClientMessageParser:

    def arrayToString(self, array):
        if not array:
            return ""
        a = array.copy()
        s = ""
        while len(a) > 1:
            s += a.pop() + ";"
        s += a.pop()
        return s

    def parse(self, msg):
        prefix = "" # change to None?
        command = ""  #""
        params = []
        msg = str(msg)
        # Remove the " b'...' "
        msg = msg[2:-1]
        if len(msg) < 1:
            return "UNKNOWN", "UNKNOWN", "UNKNOWN"
        # We have an optional prefix
        msg = msg.split(";")
        if msg[0][0] == ":":
            prefix = msg[0][1:]
            command = msg[1]
            params = msg[2:]
        else:
            command = msg[0]
            params = msg[1:]
        return prefix, command, params


class ServerMessageParser:

    def parse(self, byteMessage):
        msg = str(byteMessage)
        return msg[2:-1]

    def stringToArray(self, text):
        text = str(text)
        return text.split(";")