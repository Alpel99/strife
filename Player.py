import json
from constants import *

class Player():
    def __init__(self, id, side):
        self.id = id
        self.side = side # False: "left", True: "right"
        x = 50 if not self.side else 1870
        self.pos = [x, 0.7*H_ARR[0]]
        self.state = 0
        self.vel = [0,0]
        self.input = {"up":0,"right":0,"left":0,"down":0,"space":0}
        self.jumping = True
        self.blocking = False
        self.attacking = False
        self.ducking = False

    def getDict(self):
        player = {
            "side": self.side,
            "pos": self.pos,
            "state": self.state,
            "vel": self.vel,
            "blocking": self.blocking
        }
        return player
    
    def processInput(self):
        if(self.input["right"] == 1 and self.vel[0] < MAX_VELOCITY):
            self.vel[0] += X_ACCELERATION
        if(self.input["left"] == 1 and self.vel[0] > -MAX_VELOCITY):
            self.vel[0] -= X_ACCELERATION
        if(self.input["right"] == self.input["left"] and abs(self.vel[0]) > 0):
            change = 2*X_ACCELERATION if abs(self.vel[0]) >= 2*X_ACCELERATION else self.vel[0]
            change = -change if self.vel[0] < 0 else change
            self.vel[0] = self.vel[0] - change
        if(self.input["up"] == 1):
            self.vel[0] = 0
            self.blocking = True
        else:
            self.blocking = False

        if(self.input["space"] == 1 and not self.jumping):
            self.vel[1] -= JUMP_STRENGTH
            self.jumping = True

        self.vel[1] += GRAVITY
        pass

    def death(self):
        self.__init__(self.id, self.side)