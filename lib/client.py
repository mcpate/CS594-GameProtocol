__author__ = 'MCP'


import sys
sys.path.append('..')

import socket
from time import sleep
import logging
#logging.basicConfig(level=logging.DEBUG)
from lib.game import Player
from lib.game import Pile
from lib.message import ServerMessageParser


class Client:

    def __init__(self, socket, maxReceive):
        self.socket = socket
        self.maxReceive = maxReceive
        self.msgParser = ServerMessageParser()

    def getDiscard(self, playerName, gameName):
        return self.send(":{0};GETDISCARD;{1}".format(playerName, gameName))

    def getGames(self):
        return self.send("LIST;")

    def getHand(self, playerName, gameName):
        return self.send(":{0};GETHAND;{1}".format(playerName, gameName))

    def getUserInput(self, promptText):
        val = input(promptText)
        while not val:
            val = input("Error, no text received - {}".format(promptText))
        return val

    def registerGame(self, playerName, gameName):
        return self.send(":{0};CREATE;{1}".format(playerName, gameName))

    def registerPlayer(self, name):
        return self.send("REGISTER;{}".format(name))

    def joinGame(self, playerName, gameName):
        return self.send(":{0};JOIN;{1}".format(playerName, gameName))

    def pollForStatusOfPlay(self, playerName, gameName):
        return self.send(":{0};STATUSOFPLAY;{1}".format(playerName, gameName))

    def pollForGameStart(self, playerName, gameName):
        response = self.send(":{0};STARTGAME;{1}".format(playerName, gameName))
        while response != "OK":
            sleep(3)
            response = self.send(":{0};STARTGAME;{1}".format(playerName, gameName))
        return response

    def pollForTurn(self, playerName, gameName):
        response = self.send(":{0};TURN;{1}".format(playerName, gameName))
        while response != "OK":
            sleep(3)
            response = self.send(":{0};TURN;{1}".format(playerName, gameName))
        return response

    def play(self, playerName, card):
        return self.send(":{0};PLAY;{1}".format(playerName, card))

    def send(self, msg):
        logging.debug(msg)
        self.socket.send(bytes(msg, 'ascii'))
        response = self.msgParser.parse(self.socket.recv(self.maxReceive))
        logging.debug(response)
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

    print("Waiting for other player to join and game to start...")
    gameStart = client.pollForGameStart(playerName, gameName)

    # Game loop
    statusOfPlay = ""
    self = Player('DummyVar', 'DummyVar')
    while statusOfPlay != "GAMEOVER":
        print("Game beginning!")

        print("Waiting for turn...")
        turn = client.pollForTurn(playerName, gameName)

        #discard = client.getDiscard(playerName, gameName)
        hand = client.getHand(playerName, gameName)

        while hand != "EMPTY":
            print("Here are your cards: {}".format(hand))
            toPlay = client.getUserInput("Select a card to play: ")
            client.play(playerName, toPlay)

         #   statusOfPlay = client.pollForStatusOfPlay(playerName, gameName)

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

    clientSocket.close()