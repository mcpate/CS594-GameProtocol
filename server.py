__author__ = 'MCP'


import socket


class Game:

    name = ""
    players = []
    deck = ["2C", "3C", "4C", "5C" "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC", "AC",
            "2D", "3D", "4D", "5D" "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD", "AD",
            "2S", "3S", "4S", "5S" "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS", "AS",
            "2H", "3H", "4H", "5H" "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH", "AH"]


class ServerMessageHandler:

    def __init__(self, players, games):
        self.players = players
        self.games = games

    def handle(self, clientsocket, msg):
        print("(handler) message received: {}".format(msg))

        prefix, command, params = self.parse(msg)

        if command == "REGISTER":
            print("(handler) handling message: REGISTER")
            if params[0] in self.players:
                clientsocket.send(b'ERROR')
            else:
                print("(handler) adding new player {} to registry.".format(params[0]))
                self.players[params[0]] = None
                print("(handler) global registry: {}".format(self.players))
                clientsocket.send(b'OK')

        elif command == "JOIN":
            print("(handler) handling message: JOIN")
            if params[0] not in self.games:
                clientsocket.send(b"ERROR")
            else:
                if len(self.games[params[0]].players) > 2:
                    clientsocket.send(b'ERROR')
                else:
                    self.games[params[0]].players.append(params[0])
                    print("(handler) registering {0} with game {1}".format(prefix, params[0]))
                    clientsocket.send(b'OK')

        elif command == "LIST":
            print("(handler) handling message: LIST")
            gamelist = ""
            for game in self.games:
                if game.players <= 1:
                    gamelist += game.name
            print("(handler) sending game list: {}".format(gamelist))
            clientsocket.send(bytes(gamelist, 'ascii'))

        elif command == "CREATE":
            print("(handler) handling message: CREATE")
            if params[0] in self.games:
                clientsocket.send(b'ERROR')
            else:
                print("(handler) creating new game {0} for player {1}".format(params[0], prefix))
                newGame = Game()
                newGame.players.append(prefix)
                print("(handler) updating player {0}'s current assigned game to {1}.".format(prefix, params[0]))
                self.players[prefix] = params[0]
                self.games[params[0]] = newGame
                clientsocket.send(b'OK')

        else:
            print("(handler) ERROR: Unknown message: ".format(msg))


    def parse(self, msg):
        prefix = ""
        command = ""
        params = []
        msg = str(msg)
        # Remove the " b'...' "
        msg = msg[2:-1] #trim here seems to not be needed now?
        print("(handler) trimmed message to: {}".format(msg))
        # We have an optional prefix
        msg = msg.split(";")
        if msg[0][0] == ":":
            prefix = msg[0][1:]
            command = msg[1]
            params = msg[2:]
        else:
            command = msg[0]
            params = msg[1:]
        print("(handler) parsed message to: {} - {} - {}".format(prefix, command, params))
        return prefix, command, params




if __name__ == "__main__":
    players = {}
    games = {}
    maxData = 1024

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('localhost', 9999))

    print("socket bound to port 9999")

    serversocket.listen(5)

    print ("socket listening for connections")

    handler = ServerMessageHandler(players, games)

    while True:



        (clientsocket, address) = serversocket.accept()
        print("got a connection from {}".format(address))

        data = clientsocket.recv(maxData)
        if data:
            handler.handle(clientsocket, data)

        clientsocket.close()









