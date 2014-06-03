__author__ = 'MCP'


import sys
sys.path.append('..')

import socket
import select
from lib.game import Player
from lib.game import Game
from lib.message import ClientMessageParser


class ServerMessageHandler:

    def __init__(self, players, games):
        self.players = players
        self.games = games
        self.msgParser = ClientMessageParser()

    def handle(self, clientSocket, msg):
        #print("(handler) message received: {}".format(msg))

        prefix, command, params = self.msgParser.parse(msg)

        if command == "REGISTER":
            print("(handler) handling message: REGISTER")
            player_name = params[0]
            if player_name in self.players:
                clientSocket.send(b'ERROR')
            else:
                print("(handler) adding new player {} to registry.".format(player_name))
                self.players[player_name] = Player(player_name, clientSocket)
                #print("(handler) global player registry: {}".format(self.players))
                clientSocket.send(b'OK')

        elif command == "JOIN":
            print("(handler) handling message: JOIN")
            if params[0] not in self.games:
                clientSocket.send(b"ERROR")
                print("(handler) ERROR: game not found")
            else:
                game = self.games[params[0]]
                if game.numPlayers() == 2:
                    clientSocket.send(b'ERROR')
                    print("(handler) ERROR: game full")
                else:
                    player = self.players[prefix]
                    player.gameName = game.name
                    game.addPlayer(player)
                    print("(handler) registering {0} with game {1}".format(prefix, params[0]))
                    clientSocket.send(b'OK')

        elif command == "LIST":
            print("(handler) handling message: LIST")
            gameList = self.findOpenGames()
            gameString = self.msgParser.arrayToString(gameList)
            if not gameString:
                print("handler) no open games found")
                clientSocket.send(b'ERROR')
            else:
                print("(handler) sending game list '{0}' to '{1}'".format(gameString, clientSocket.getpeername()))
                clientSocket.send(bytes(gameString, 'ascii'))

        elif command == "CREATE":
            print("(handler) handling message: CREATE")
            gameName = params[0]
            if gameName in self.games:
                clientSocket.send(b'ERROR')
            else:
                creator = self.players[prefix]
                print("(handler) creating new game '{0}' for player '{1}'".format(gameName, prefix))
                newGame = Game(gameName, creator)
                creator.game = newGame
                self.games[gameName] = newGame
                #print("(handler) global game registry: {}".format(self.games))
                clientSocket.send(b'OK')

        elif command == "GETHAND":
            print("(handler) handling message: GETHAND")
            player = self.players[prefix]
            print("(handler) building string response for hand: {}".format(player.inHand))
            cardString = self.msgParser.arrayToString(player.inHand)
            print("(handler) sending '{}' to client".format(cardString))
            clientSocket.send(bytes(cardString, 'ascii'))

        elif command == "STARTGAME":
            game = self.games[params[0]]
            print(game)
            print("(handler) received request to start game '{0}' from '{1}'".format(game.name, prefix))
            if len(game.players) < 2:
                clientSocket.send(b'ERROR')
            elif game.inProgress:
                clientSocket.send(b'OK')
            else:
                print("(handler) beginning game {}".format(game.name))
                print(game.players[0].name, game.players[1].name)
                game.beginGame()
                clientSocket.send(b'OK')

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
                    clientSocket.send(b'LOOSE')
                    opponent.socket.send(b'WIN')
                elif game.currentPlay[0] < params[0][0]:
                    print("(handler) WIN/LOOSE")
                    clientSocket.send(b'WIN')
                    opponent.socket.send(b'LOOSE')
                else:
                    print("(handler) TIE/TIE")
                    clientSocket.send(b'TIE')
                    opponent.socket.send(b'TIE')
                game.currentPlay = None

        else:
            print("(handler) ERROR: Unknown message: ".format(msg))
            #aise Exception

    def findOpenGames(self):
        gameList = []
        for game in self.games:
                if self.games[game].numPlayers() < 2:
                    gameList.append(game)
        return gameList




if __name__ == "__main__":
    players = {}  # name : gamename
    games = {}  # gamename : gameobject
    handler = ServerMessageHandler(players, games)
    connections = []
    MAX_RECV = 1024

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 9999))
    server.listen(5)
    print("server socket bound to 'localhost:9999' and listening for connections")

    connections.append(server)

    while True:

        # Poll the connection list for sockets that have incoming data.
        read_sockets, _, _ = select.select(connections, [], [])

        for sock in read_sockets:

            # New connection.
            if sock == server:
                client, address = server.accept()
                connections.append(client)
                print("\ngot a connection from '{}'".format(address))

            # Message for an already connected client.
            else:
                try:
                    data = sock.recv(MAX_RECV)

                    # Not sure why this case started happening randomly..
                    if data == b'':
                        print("\nconnection broken to '{}'".format(sock.getpeername()))
                        sock.close()
                        connections.remove(sock)
                    else:
                        print("\nreceived data from {}".format(sock.getpeername()))
                        handler.handle(sock, data)

                except ConnectionError:
                    print("lost a connection from {0}.".format(sock.getpeername()))
                    sock.close()
                    connections.remove(sock)
                    continue

    server.close()









