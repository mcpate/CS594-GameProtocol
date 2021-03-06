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
from lib.game import Card


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

    def pollForOpponentMove(self, playerName, gameName):
        response = self.send(":{0};OPPONENTMOVE;{1}".format(playerName, gameName))
        while response == "ERROR":
            sleep(3)
            response = self.send(":{0};OPPONENTMOVE;{1}".format(playerName, gameName))
        return response

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
    msgParser = ServerMessageParser()
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
    winCount = 0
    tieCount = 0
    lossCount = 0
    print("Game beginning!")
    statusOfPlay = ""
    self = Player('DummyVar', 'DummyVar')
    while statusOfPlay != "GAMEOVER":

        #discard = client.getDiscard(playerName, gameName)
        hand = msgParser.stringToArray(client.getHand(playerName, gameName))
        if hand[0] == "EMPTY":
            statusOfPlay = "GAMEOVER"
            break

        print("Waiting for turn...")
        turn = client.pollForTurn(playerName, gameName)

        #while hand != "EMPTY":
        print("Here are your cards: {}".format(hand))
        toPlay = client.getUserInput("Select a card to play: ")
        while toPlay not in hand:
            toPlay = client.getUserInput("Select a card to play: ")

        client.play(playerName, toPlay)
        clientCard = Card(toPlay)

        print("Waiting for your opponent to play...")
        opponentMove = client.pollForOpponentMove(playerName, gameName)
        opponentCard = Card(opponentMove)

        print("You played '{0}' - Your opponent played '{1}'.".format(clientCard.value, opponentCard.value))
        if clientCard.compare(opponentCard) == 1:
            print("You win!")
            winCount += 1
        elif clientCard.compare(opponentCard) == 0:
            print("You tie!")
            tieCount += 1
        else:
            print("You lose!")
            lossCount += 1

    if (winCount + tieCount) > lossCount:
        print("You win the overall count!  Congrats!\nGAME OVER.")
    else:
        print("You lose the overall count.\nGAME OVER.")

    clientSocket.close()