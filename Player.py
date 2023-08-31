import json

class Player():
    def __init__(self, id) -> None:
        self.id = id
        self.side = False # 0 -> left
        x = 50 if not self.side else 1870
        self.position = [x, 550]
        self.state = 0
        self.vel = [0,0]

    def getDict(self):
        player = {
            "side": self.side,
            "position": self.position,
            "state": self.state,
            "vel": self.vel,
        }
        return player