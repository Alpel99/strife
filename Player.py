import json
import time
from constants import *

class Player():
    def __init__(self, id, side):
        self.id = id
        self.side = side # False: "left", True: "right"
        self.facing = not side
        x = 50 if not self.side else 1870
        self.pos = [x, 0.7*H_ARR[0]]
        self.vel = [0,0]
        self.input = {"up":0,"right":0,"left":0,"down":0,"space":0,"attack": 0,"dash":0}
        self.jumping = True
        self.dashing = 0
        self.attack_time = time.time()
        self.dash_time = time.time()
        self.state = 0
        """
        0: default
        1: blocking
        2: attacking
        3: ducking
        """

    def getDict(self):
        player = {
            "side": self.side,
            "pos": self.pos,
            "state": self.state,
            "vel": self.vel,
            "facing": self.facing,
        }
        return player
    
    def processInput(self):
        self.state = 0
        # x vel input
        if(self.input["right"]):
            self.facing = True
            self.vel[0] += X_ACCELERATION
        if(self.input["left"]):
            self.facing = False
            self.vel[0] -= X_ACCELERATION
        # constrain speed
        self.vel[0] = min(MAX_VELOCITY, max(-MAX_VELOCITY, self.vel[0]))
        # slow down/stand still on no/blocking input
        if(self.input["right"] == self.input["left"] and abs(self.vel[0]) > 0):
            change = 2*X_ACCELERATION if abs(self.vel[0]) >= 2*X_ACCELERATION else abs(self.vel[0])
            change = -change if self.vel[0] < 0 else change
            self.vel[0] = self.vel[0] - change
        # jump
        if(self.input["space"] == 1 and not self.jumping):
            self.vel[1] -= JUMP_STRENGTH
            self.jumping = True
        # block
        if(self.input["up"]):
            self.vel[0] = 0
            self.state = 1
        # duck
        if(self.input["down"]):
            self.vel[0] = self.vel[0] if abs(self.vel[0]) < MAX_VELOCITY else MAX_VELOCITY/2 if self.vel[0] > 0 else -MAX_VELOCITY/2
            self.state = 2
        # attack
        if(self.input["attack"]):
            self.state = 3
        # low attack
        if(self.input["attack"] and self.input["down"]):
            self.state = 5
        # dash
        if((self.input["dash"]) or self.dashing != 0) and self.dashing < DASH_DUR:
            # print(self.dashing)
            self.dashing += 1
            dash_vel = DASH_SPEED if self.facing else -DASH_SPEED
            self.vel = [dash_vel, 0]
            self.state = 4
        # dash attack
        if(self.input["dash"] and self.input["attack"]):
            self.state = 6
        # dash block
        if(self.input["dash"] and self.input["up"]):
            self.state = 7

        self.vel[1] += GRAVITY
        pass

    def death(self):
        self.__init__(self.id, self.side)