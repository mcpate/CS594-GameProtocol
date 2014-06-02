__author__ = 'MCP'


import socket
import select


class Game:

    name = ""
    players = []
    deck = ["2C", "3C", "4C", "5C" "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC", "AC",
            "2D", "3D", "4D", "5D" "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD", "AD",
            "2S", "3S", "4S", "5S" "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS", "AS",
            "2H", "3H", "4H", "5H" "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH", "AH"]
    discard = []
    inProgress = False

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
        for _ in range(2):
            player1.faceDown.append(deck.pop)
            player2.faceDown.append(deck.pop)
        for _ in range(2):
            player1.faceUp.append(deck.pop)
            player2.faceUp.append(deck.pop)
        for _ in range(2):
            player1.inHand.append(deck.pop)
            player2.inHand.append(deck.pop)
        discard.append(deck.pop)



class Player:

    faceDown = []
    faceUp = []
    inHand = []

    def __init__(self, name, socket):
        self.name = name
        self.socket = socket
        self.gameName = ""


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
                self.players[params[0]] = Player(params[0], clientsocket)
                print("(handler) global player registry: {}".format(self.players))
                clientsocket.send(b'OK')

        elif command == "JOIN":
            print("(handler) handling message: JOIN")
            if params[0] not in self.games:
                clientsocket.send(b"ERROR")
            else:
                if len(self.games[params[0]].players) > 2:
                    clientsocket.send(b'ERROR')
                else:
                    player = self.players[prefix]
                    self.games[params[0]].players.append(player)
                    print("(handler) registering {0} with game {1}".format(prefix, params[0]))
                    clientsocket.send(b'OK')

        elif command == "LIST":
            print("(handler) handling message: LIST")
            gamelist = ";"
            for game in self.games:
                assert isinstance(self.games[game].players, list)
                if len(self.games[game].players) <= 1:
                    gamelist += (game + ";")
            print("(handler) sending game list: {0} to: {1}".format(gamelist, clientsocket.getpeername()))
            clientsocket.send(bytes(gamelist, 'ascii'))

        elif command == "CREATE":
            print("(handler) handling message: CREATE")
            if params[0] in self.games:
                clientsocket.send(b'ERROR')
            else:
                print("(handler) creating new game {0} for player {1}".format(params[0], prefix))
                newGame = Game()
                player = self.players[prefix]
                newGame.players.append(player)
                print("(handler) updating player {0}'s current assigned game to {1}.".format(prefix, params[0]))
                self.players[prefix] = params[0]
                self.games[params[0]] = newGame
                print("(handler) global game registry: {}".format(self.games))
                clientsocket.send(b'OK')

        elif command == "STARTGAME":
            print("(handler) received request to start game '{0}' from '{1}'".format(params[0], prefix))
            # Check if the game is legit and has right amount of players.
            game = params[0]
            if not self.games[game] or len(self.games[game].players) < 2:
                clientsocket.send(b'ERROR')
            elif self.games[game].inProgress:
                clientsocket.send(b'OK')
            else:
                self.games[game].beginGame()
                clientsocket.send(b'OK')


        else:
            print("(handler) ERROR: Unknown message: ".format(msg))
            #aise Exception


    def parse(self, msg):
        prefix = ""
        command = ""
        params = []
        msg = str(msg)
        # Remove the " b'...' "
        msg = msg[2:-1] #trim here seems to not be needed now?
        print("(handler) trimmed message to: {}".format(msg))
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
        print("(handler) parsed message to: {} - {} - {}".format(prefix, command, params))
        return prefix, command, params




if __name__ == "__main__":
    players = {}  # name : gamename
    games = {}  # gamename : gameobject
    handler = ServerMessageHandler(players, games)
    connections = []
    MAX_RECV = 1024

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('localhost', 9999))
    print("socket bound to port 9999")
    serversocket.listen(5)
    print("socket listening for connections")

    connections.append(serversocket)

    while True:

        # Poll the connection list for sockets that have incoming data.
        read_sockets, _, _ = select.select(connections, [], [])

        for sock in read_sockets:

            # New connection.
            if sock == serversocket:
                clientsocket, address = serversocket.accept()
                connections.append(clientsocket)
                print("\ngot a connection from {}".format(address))

            # Message for an already connected client.
            else:
                try:
                    data = sock.recv(MAX_RECV)
                    # Not sure why this case started happening randomly..
                    if data == b'':
                        print("\nconnection broken to {}".format(sock.getpeername()))
                        connections.remove(sock)
                    else:
                        print("\nreceived data from {}".format(sock.getpeername()))
                        handler.handle(sock, data)
                except:
                    print("lost a connection from {0} with error {1}".format(sock.getpeername()))
                    sock.close()
                    connections.remove(sock)
                    continue

    serversocket.close()









