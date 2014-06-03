__author__ = 'MCP'


import socket
import select
from lib.game import Player



class ServerMessageHandler:

    def __init__(self, players, games):
        self.players = players
        self.games = games

    def handle(self, clientsocket, msg):
        print("(handler) message received: {}".format(msg))

        prefix, command, params = self.parse(msg)

        if command == "REGISTER":
            print("(handler) handling message: REGISTER")
            player_name = params[0]
            if player_name in self.players:
                clientsocket.send(b'ERROR')
            else:
                print("(handler) adding new player {} to registry.".format(player_name))
                self.players[player_name] = Player(player_name, clientsocket)
                print("(handler) global player registry: {}".format(self.players))
                clientsocket.send(b'OK')

        elif command == "JOIN":
            print("(handler) handling message: JOIN")
            game = self.games[params[0]]
            if params[0] not in self.games:
                clientsocket.send(b"ERROR")
            else:
                print("(handler) '{0}' requesting to JOIN '{1}'".format(prefix, game.name))
                if len(self.games[params[0]].players) == 2:
                    clientsocket.send(b'ERROR')
                else:
                    player = self.players[prefix]
                    player.gameName = game.name
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
            game_name = params[0]
            if game_name in self.games:
                clientsocket.send(b'ERROR')
            else:
                print("(handler) creating new game {0} for player {1}".format(game_name, prefix))
                newGame = Game()
                newGame.name = game_name
                player = self.players[prefix]
                player.gameName = game_name
                newGame.players.append(player)
                self.games[game_name] = newGame
                print("(handler) global game registry: {}".format(self.games))
                clientsocket.send(b'OK')

        elif command == "GETHAND":
            print("(handler) handling message: GETHAND")
            player = self.players[prefix]
            print("(handler) building string response for hand: {}".format(player.inHand))
            cardString = self.arrayToString(player.inHand)
            print("(handler) sending '{}' to client".format(cardString))
            clientsocket.send(bytes(cardString, 'ascii'))

        elif command == "STARTGAME":
            game = self.games[params[0]]
            print(game)
            print("(handler) received request to start game '{0}' from '{1}'".format(game.name, prefix))
            if len(game.players) < 2:
                clientsocket.send(b'ERROR')
            elif game.inProgress:
                clientsocket.send(b'OK')
            else:
                print("(handler) beginning game {}".format(game.name))
                print(game.players[0].name, game.players[1].name)
                game.beginGame()
                clientsocket.send(b'OK')

        elif command == "PLAY":
            print("(handler) handling message: PLAY")
            player = self.players[prefix]
            game_name = player.gameName
            game = self.games[game_name]
            opponent = game.getOpponent(player)
            print("(handler) '{0}' playing '{1}'".format(player.name, params[0]))
            if game.currentPlay is None:
                print("(handler) first play")
                game.currentPlay = params[0]
            else:
                if game.currentPlay[0] > params[0][0]:
                    print("(handler) LOOSE/WIN")
                    clientsocket.send(b'LOOSE')
                    opponent.socket.send(b'WIN')
                elif game.currentPlay[0] < params[0][0]:
                    print("(handler) WIN/LOOSE")
                    clientsocket.send(b'WIN')
                    opponent.socket.send(b'LOOSE')
                else:
                    print("(handler) TIE/TIE")
                    clientsocket.send(b'TIE')
                    opponent.socket.send(b'TIE')
                game.currentPlay = None

        else:
            print("(handler) ERROR: Unknown message: ".format(msg))
            #aise Exception

    def arrayToString(self, array):
        a = array.copy()
        s = ""
        while len(a) > 1:
            s += a.pop() + ";"
        s += a.pop()
        return s

    def parse(self, msg):
        prefix = ""
        command = ""
        params = []
        msg = str(msg)
        # Remove the " b'...' "
        msg = msg[2:-1] #trim here seems to not be needed now?
        #print("(handler) trimmed message to: {}".format(msg))
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
        #print("(handler) parsed message to: {} - {} - {}".format(prefix, command, params))
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
                except ConnectionError:
                    print("lost a connection from {0}.".format(sock.getpeername()))
                    sock.close()
                    connections.remove(sock)
                    continue

    serversocket.close()









