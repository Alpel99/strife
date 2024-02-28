from perlin_noise import PerlinNoise
import random

from Player import Player
from constants import *

class Gamestate():
    def __init__(self):
        self.terrain = self.generateTerrain()
        print(self.terrain)
        self.platforms = self.generatePlatforms()
        print(self.platforms)
        self.players = {}
        self.global_score = 0
        self.left_score = 0
        self.right_score = 0
        self.side_delta = 0

    def getData(self):
        gamestate = {
            "id": 0,
            "terrain": self.terrain,
            "platforms": self.platforms,
            "players": [p.getDict() for p in self.players.values()],
            "global_score": self.global_score,
            "left_score": self.left_score,
            "right_score": self.right_score
        }
        # return json.dumps(gamestate)
        return gamestate
    
    def addPlayer(self, client_id):
        side = bool(random.getrandbits(1)) if self.side_delta == 0 else True if self.side_delta < 0 else False
        self.side_delta = self.side_delta +1 if side else self.side_delta - 1
        player = Player(client_id, side)
        self.players[client_id] = player

    def removePlayer(self, client_id):
        self.side_delta = self.side_delta +1 if not self.players[client_id].side else self.side_delta - 1
        del self.players[client_id]

    def win(self, client_id):
        side = self.players[client_id].side
        self.global_score = self.global_score +1 if side else self.global_score - 1
        self.left_score = 0
        self.right_score = 0 
        self.terrain = self.generateTerrain()
        self.platforms = self.generatePlatforms()
        for p in self.players.values():
            p.__init__(p.id, p.side)

    def kill(self, player_id):
        p = self.players[player_id]
        if(p.side):
            self.left_score += 1
        else:
            self.right_score += 1
        p.__init__(p.id, p.side)

    def generateTerrain(self):
        noise = PerlinNoise(octaves=7, seed=random.randint(0,MAX_RNDM))
        steps = int((WIDTH-(PLATFORM_WIDTH*2))/NOISE_STEPS)
        res = [noise(s)*NOISE_MULTIPLIER for s in [i/steps for i in range(steps)]]
        res = [min(e+0.3, 1) for e in res]
        res = [max(e, MIN_HEIGHT) for e in res]

        p = [[0,int(0.5*TERRAIN_BDRY[1])] for _ in range(PLATFORM_WIDTH)]
        return p + [[0,300] for _ in range(int((WIDTH-(PLATFORM_WIDTH*2))))] + p
    
    def generatePlatforms(self):
        oct = 2
        bot_noise = PerlinNoise(octaves=oct, seed=random.randint(0,MAX_RNDM))
        thick_noise = PerlinNoise(octaves=oct, seed=random.randint(0,MAX_RNDM))
        steps = int((WIDTH-(PLATFORM_WIDTH*2))/NOISE_STEPS)
        bot = [abs(bot_noise(s)) for s in [i/steps for i in range(steps)]]
        thick = [abs(thick_noise(s)) for s in [i/steps for i in range(steps)]]
        thick = [min(e, 1) for e in thick]
        thick = [max(e, 0) for e in thick]
        bot = [min(e, 1) for e in bot]
        bot = [max(e, 0) for e in bot]
        r = [[0,0] for _ in range(0, steps)]
        p = [[0,0] for _ in range(0, PLATFORM_WIDTH)]
        maxh = abs(PLATFORM_BDRY[0] - PLATFORM_BDRY[1])
        for i,(b,t) in enumerate(zip(bot, thick)):
            if t > 0.1:
                # print(i,b,t)
                r[i] = [int(b*maxh/2+PLATFORM_BDRY[0]),int(t*maxh/2)]
        res = p + [item for item in r for _ in range(NOISE_STEPS)] + p
        # return [[700, 800] for x in range(steps)]
        return res

if __name__ == "__main__":
    gs = Gamestate()
    gs.generateTerrain()
    print(gs.terrain)
