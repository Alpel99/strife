import json

class Gamestate():
    def __init__(self) -> None:
        self.terrain = [1]*1920
        self.players = {}
        self.global_score = 0
        self.left_score = 0
        self.right_score = 0

    def getData(self):
        gamestate = {
            "id": 0,
            "terrain": self.terrain,
            "players": [p.getDict() for p in self.players.values()],
            "global_score": self.global_score,
            "left_score": self.left_score,
            "right_score": self.right_score
        }
        # return json.dumps(gamestate)
        return gamestate
    
    def addPlayer(self, player):
        self.players[player.id] = player

     
     
