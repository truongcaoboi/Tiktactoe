from flask import Flask
from flask import Flask
from flask_restful import Api, Resource, reqparse, request
from flask_cors import CORS
import json
from controller.GameController import CreatorGame, FoldGame, PlayGame
app = Flask(__name__)

api = Api(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# argument parsing
parser = reqparse.RequestParser()
parser.add_argument('query')


api.add_resource(CreatorGame, '/api/game/creategame/<int:idGame>')
api.add_resource(FoldGame, "/api/game/foldgame/<int:idGame>")
api.add_resource(PlayGame, "/api/game/playgame/<int:idGame>/<int:action>")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
