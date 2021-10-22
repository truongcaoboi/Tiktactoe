from flask import Flask
from flask_restful import Api, Resource, reqparse, request
from logic.Game import Game

listgame = []

class CreatorGame(Resource):
    def get(self, idGame):
        if(idGame == 0):
            game = Game(len(listgame)+1)
            listgame.append(game)
        else:
            for g in listgame:
                if(g.idGame == idGame):
                    game = g
        data = game.reset()
        return data

class FoldGame(Resource):
    def get(self, idGame):
        for game in listgame:
            if(game.idGame == idGame):
                data = {}
                if(game.gameOver):
                    data["message"] = "Game is finished!"
                else:
                    game.foldGame()
                    data["message"] = "You lost!"
                return data, 200

class PlayGame(Resource):
    def get(self, idGame, action):
        data = {}
        for game in listgame:
            if(game.idGame == idGame):
                if(game.gameOver):
                    data["message"] = "Game is finished!"
                else:
                    data1 = game.step(action)
                    data2 = None
                    if(game.isAuto and not game.gameOver and data1["mark"] != -1):
                        data2 = game.stepAuto()
                    data["player1"] = data1
                    data["player2"] = data2
                    data["message"] = "Ok"
                return data, 200
        data["message"] = "Not found game!"
        return data, 200
