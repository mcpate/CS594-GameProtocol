__author__ = 'MCP'


import socket
from time import sleep

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
        serverResponse = serverResponse.split(";")
        if len(serverResponse[1]) == 0:
            return []
        else:
            return serverResponse[1:]

    def registerGame(self, gamename, playername, socket):
        print("(client) registering new game: {}".format(gamename))
        socket.send(bytes(":{0};CREATE;{1}".format(playername, gamename), 'ascii'))
        serverResponse = self.parse(socket.recv(maxData))
        print("(client) server response: {}".format(serverResponse))
        return serverResponse

    def joinGame(self, gamename, playername, socket):
        print("(client) joining game: {}".format(gamename))
        socket.send(bytes(":{0};JOIN;{1}".format(playername, gamename), 'ascii'))
        serverResponse = self.parse(socket.recv(maxData))
        print("(client) server response: {}".format(serverResponse))
        return serverResponse

    def waitForGameStart(self, playername, gamename, socket):
        print("(client) waiting (polling) for game start")
        msg = ":{0};STARTGAME;{1}".format(playername, gamename)
        try:
            socket.send(bytes(msg, 'ascii'))
            data = socket.recv(maxData)
            while self.parse(data) != "OK":
                print("(client) polling...")
                print("(client) message received: {}".format(data))
                sleep(3)
                socket.send(bytes(msg, 'ascii'))
                data = socket.recv(maxData)
        except BrokenPipeError as e:
            print("(client) broken pipe with error: {}".format(e))

        print("(client) game beginning")



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
        playername = str(input("Please enter a nickname to use: "))
        while len(playername) == 0:
            playername = str(input("Please enter a nickname to use: "))

        response = client.registerPlayername(playername, clientsocket)

    gamenames = client.getGames(clientsocket)
    gamename = ""
    if len(gamenames) == 0:
        while len(gamename) == 0:
            gamename = input("Currently there are no running games.\nPlease list the name of a game to create: ")
        client.registerGame(gamename, playername, clientsocket)
    else:
        print("Here are the available games: {}".format(gamenames))
        gamename = ""
        while len(gamename) == 0:
            gamename = input("Please select one to join or type a new name to create a game: ")
        if gamename in gamenames:
            client.joinGame(gamename, playername, clientsocket)
        else:
            client.registerGame(gamename, playername, clientsocket)


    null = client.waitForGameStart(playername, gamename, clientsocket)

    #client.playGame(clientsocket)


    clientsocket.close()




