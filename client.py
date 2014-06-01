__author__ = 'MCP'


import socket


class Client:

    def registerPlayername(self, name, socket):
        print("(client) registering playername: {}".format(name))
        socket.send(bytes("REGISTER;{}".format(name), 'ascii'))
        serverResponse = self.parse(socket.recv(maxData))
        print("(client) server response: {}".format(serverResponse))
        return serverResponse

    def parse(self, byteMessage):
        msg = str(byteMessage)
        return msg[2:-1]

    def getGames(self, socket):
        print("(client) requesting the list of games.")
        socket.send(b"LIST;")
        serverResponse = self.parse(socket.recv(maxData))
        print("(client) server response: {}".format(serverResponse))
        return serverResponse

    def registerGame(self, gamename, playername, socket):
        print("(client) registering new game: {}".format(gamename))
        socket.send(bytes(":{0};CREATE;{1}".format(playername, gamename), 'ascii'))
        serverResponse = self.parse(socket.recv(maxData))
        print("(client) server response: {}".format(serverResponse))
        return serverResponse



if __name__ == "__main__":
    maxData = 1024
    client = Client()

    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('localhost', 9999))
    print("socket connected to port 9999")

    print("Welcome to 3Up3Down!")

    response = ""
    playername = ""
    while response != "OK":
        while len(playername) == 0:
            playername = str(input("Please enter a nickname to use: "))
        response = client.registerPlayername(playername, clientsocket)
    clientsocket.close()

    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('localhost', 9999))
    gamenames = client.getGames(clientsocket)
    clientsocket.close()

    if len(gamenames) == 0:
        newGamename = ""
        while len(newGamename) == 0:
            newGamename = input("Currently there are no running games.\n"
                                "Please list the name of a game to create: ")
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect(('localhost', 9999))
        client.registerGame(newGamename, playername, clientsocket)
        clientsocket.close()
    else:
        print("Here are the available games: {}".format(gamenames))
