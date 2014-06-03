__author__ = 'MCP'


import sys
sys.path.append('..')

import socket
from time import sleep
import logging


class Client:  # creat a lambda here that prints sending message and receiving message
                # and sends into socket/receives from socket?  should shorten methods...
    def __init__(self, socket, maxReceive):
        self.socket = socket
        self.maxReceive = maxReceive

    def registerPlayer(self, name):
        return self.send("REGISTER;{}".format(name))

    def parse(self, byteMessage):
        msg = str(byteMessage)
        return msg[2:-1]

    def getDiscard(self, playerName, gameName, socket):
        return self.send(":{0};GETDISCARD;{1}".format(playerName, gameName))
        #print("(client) requesting discard")
        #socket.send(bytes(":{0};GETDISCARD;{1}".format(playername, gamename), 'ascii'))
        #serverResponse = self.parse(socket.recv(MAX_RECV))
        #print("(client) server response: ".format(serverResponse))
        #return serverResponse

    def getGames(self):
        return self.send("LIST;")
        #print("(client) requesting the list of games.")
        #socket.send(b"LIST;")
        #serverResponse = self.parse(socket.recv(MAX_RECV))
        #print("(client) server response: {}".format(serverResponse))
        #serverResponse = serverResponse.split(";")
        #if len(serverResponse[1]) == 0:
        #    return []
        #else:
        #    return serverResponse[1:]

    def getHand(self, playername, gamename, socket):
        print("(client) requesting hand")
        socket.send(bytes(":{0};GETHAND;{1}".format(playername, gamename), 'ascii'))
        serverResponse = self.parse(socket.recv(MAX_RECV))
        print("(client) server response: ".format(serverResponse))
        return serverResponse.split(";")

    def getUserInput(self, promptText):
        val = input(promptText)
        while not val:
            val = input("Error, no text received - {}".format(promptText))
        return val

    def registerGame(self, playerName, gameName):
        return self.send(":{0};CREATE;{1}".format(playerName, gameName))
        #print("(client) registering new game: {}".format(gamename))
        #socket.send(bytes(":{0};CREATE;{1}".format(playername, gamename), 'ascii'))
        #serverResponse = self.parse(socket.recv(MAX_RECV))
        #print("(client) server response: {}".format(serverResponse))
        #return serverResponse

    def joinGame(self, playerName, gameName):
        return self.send(":{0};JOIN;{1}".format(playerName, gameName))
        #print("(client) joining game: {}".format(gamename))
        #socket.send(bytes(":{0};JOIN;{1}".format(playername, gamename), 'ascii'))
        #serverResponse = self.parse(socket.recv(MAX_RECV))
        #print("(client) server response: {}".format(serverResponse))
        #return serverResponse

    def waitForGameStart(self, playername, gamename, socket):
        print("(client) waiting (polling) for game start")
        msg = ":{0};STARTGAME;{1}".format(playername, gamename)
        try:
            socket.send(bytes(msg, 'ascii'))
            data = socket.recv(MAX_RECV)
            while self.parse(data) != "OK":
                print("(client) polling...")
                print("(client) message received: {}".format(data))
                sleep(3)
                socket.send(bytes(msg, 'ascii'))
                data = socket.recv(MAX_RECV)
        except BrokenPipeError as e:
            print("(client) broken pipe with error: {}".format(e))
        print("(client) game beginning")

    def play(self, card, playername, gamename, socket):
        print("(client) playing card: {}".format(card))
        socket.send(bytes(":{0};PLAY;{1}".format(playername, card), 'ascii'))
        serverResponse = self.parse(socket.recv(MAX_RECV))
        print("(client) response: ".format(serverResponse))
        return serverResponse

    def send(self, msg):
        logging.debug("(client::send) sending message: ".format(msg))
        self.socket.send(bytes(msg, 'ascii'))
        response = self.parse(self.socket.recv(self.maxReceive))
        logging.debug("(client::send) received response: ".format(response))
        return response



if __name__ == "__main__":
    MAX_RECV = 1024
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect(('localhost', 9999))

    client = Client(clientSocket, MAX_RECV)

    print("socket making connection from '{0}' to 'localhost:9999'".format(clientSocket.getsockname()))
    print("\nWelcome to 3Up3Down!")

    response = ""
    playerName = ""
    while response != "OK":
        playerName = client.getUserInput("Please enter a nickname to use: ")
        response = client.registerPlayer(playerName)

    gameName = ""
    gameNames = client.getGames()
    if gameNames == "ERROR":
        gameName = client.getUserInput("Currently there are no running games - "
                                       "please list the name of a game to create: ")
        client.registerGame(playerName, gameName)
    else:
        print("Here are the available games: {}".format(gameNames))
        gameName = client.getUserInput("Please select a game to join OR type a new name to create a game: ")
        if gameName in gameNames:
            client.joinGame(playerName, gameName)
        else:
            client.registerGame(playerName, gameName)
    #
    #
    # null = client.waitForGameStart(playername, gamename, clientsocket)
    #
    # rounds = 0
    # winCount = 0
    # hand = client.getHand(playername, gamename, clientsocket)
    # while len(hand) >= 0:
    #     rounds += 1
    #     print("Beginning Round {}.".format(rounds))
    #     winRound = 0
    #     while len(hand) > 0:
    #         card = input("Here are your cards: {}\nSelect one to play: ".format(hand))
    #         hand.remove(card)
    #         status = client.play(card, playername, gamename, clientsocket)
    #         print("The results of that play are: {}".format(status))
    #     #hand

    clientsocket.close()