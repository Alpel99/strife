from perlin_noise import PerlinNoise
import random

from Player import Player
from constants import *

class Gamestate():
    def __init__(self):
        self.generateTerrain()
        self.players = {}
        self.global_score = 0
        self.left_score = 0
        self.right_score = 0
        self.side_delta = 0

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
    
    def addPlayer(self, client_id):
        side = bool(random.getrandbits(1)) if self.side_delta == 0 else False if self.side_delta < 0 else True
        self.side_delta = self.side_delta +1 if side else self.side_delta - 1
        player = Player(client_id, side)
        self.players[client_id] = player

    def removePlayer(self, client_id):
        self.side_delta = self.side_delta +1 if not self.players[client_id].side else self.side_delta - 1
        del self.players[client_id]

    def win(self, client_id):
        side = self.players[client_id].side
        self.global_score = self.global_score +1 if side else self.global_score - 1
        self.generateTerrain()
        for p in self.players.values():
            p.__init__(p.id, p.side)


    def generateTerrain(self):
        noise = PerlinNoise(octaves=5, seed=random.randint(0,2147483647))
        steps = int((WIDTH-(PLATFORM_WIDTH*2))/NOISE_STEPS)
        res = [noise(s) for s in [i/steps for i in range(steps)]]
        res = [min(e+0.3, 1) for e in res]
        res = [max(e, MIN_HEIGHT) for e in res]

        p = [0.5]*PLATFORM_WIDTH
        self.terrain = p + [item for item in res for _ in range(NOISE_STEPS)] + p
     
if __name__ == "__main__":
    gs = Gamestate()
    gs.generateTerrain()
    print(gs.terrain)
