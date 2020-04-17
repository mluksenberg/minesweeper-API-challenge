import flask_restplus

game_ns = flask_restplus.Namespace("game", description="Game endpoints")

@game_ns.route("/")
class Game(flask_restplus.Resource):

    def get(self):
        return {"test": "response"}
