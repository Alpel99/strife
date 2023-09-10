from perlin_noise import PerlinNoise
import random

from constants import *

class Gamestate():
    def __init__(self):
        # self.terrain = [1]*1920
        self.generateTerrain()
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
