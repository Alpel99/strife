import json
import time
from constants import *
from utils import circle_triangle_collision

class Player():
    def __init__(self, id, side):
        self.id = id
        self.side = side # False: "left", True: "right"
        self.facing = not side
        x = 50 if not self.side else 1870
        self.pos = [x, 0.7*H_ARR[0]]
        if id == "test":
            self.pos[0] = WIDTH/2
        self.vel = [0,0]
        self.input = {"up":0,"right":0,"left":0,"down":0,"space":0,"attack": 0,"dash":0}
        self.jumping = True
        self.dashing = 0
        self.attacking = 0
        self.state = 0
        """
        0: default
        1: blocking
        2: attacking
        3: ducking
        4: dashing
        5: duck attack
        6: dash attack
        7: dash block
        """

    def getDict(self):
        player = {
            "id": self.id,
            "side": self.side,
            "pos": self.pos,
            "state": self.state,
            "vel": self.vel,
            "facing": self.facing,
            "dashing": self.dashing,
            "attacking": self.attacking,
        }
        return player
    
    def processInput(self):
        self.state = 0
        # print(self.dashing, self.attacking)
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
            self.vel[0] = self.vel[0] if abs(self.vel[0]) < MAX_VELOCITY else MAX_VELOCITY/DUCK_SLOW_FACTOR if self.vel[0] > 0 else -MAX_VELOCITY/DUCK_SLOW_FACTOR
            self.state = 2
        # attack
        # print(self.attacking)
        if((self.input["attack"] or self.attacking != 0) and self.attacking < ATT_DUR):
            self.state = 3
            self.attacking += 1
        # low attack
        if(self.attacking > 0 and self.input["down"]):
            self.state = 5
        if(self.attacking >= ATT_DUR and self.attacking < ATT_DUR + ATT_CD):
            self.attacking += 1
        if(self.attacking >= ATT_DUR + ATT_CD):
            self.attacking = 0
        # dash
        if((self.input["dash"]) or self.dashing != 0) and self.dashing < DASH_DUR:
            # print(self.dashing)
            self.dashing += 1
            dash_vel = DASH_SPEED if self.facing else -DASH_SPEED
            self.vel = [dash_vel, 0]
            self.state = 4
        if(self.dashing >= DASH_DUR and self.dashing < DASH_DUR + DASH_CD):
            self.dashing += 1
        if(self.dashing >= DASH_DUR+DASH_CD):
            self.dashing = 0
        # dash attack
        if(self.attacking > 0 and self.attacking < ATT_DUR and self.dashing > 0 and self.dashing < DASH_DUR):
            self.state = 6
        # dash block
        if(self.dashing > 0 and self.dashing < DASH_DUR and self.input["up"]):
            self.state = 7

        self.vel[1] += GRAVITY
        pass

    def check_hit(self, other):
        p1 = [self.pos[0], self.pos[1]-PLAYER_HEIGHT]
        p2 = [self.pos[0], self.pos[1]+PLAYER_HEIGHT]
        offset = PLAYER_WIDTH+50 if self.facing else -(PLAYER_WIDTH+50)
        p3 = [self.pos[0] + offset, self.pos[1]]
        if(circle_triangle_collision(other.pos, PLAYER_WIDTH, [p1, p2, p3])):
            if other.state == 1 or other.state == 7:
                return self.id
            else:
                return other.id
        else:
            return False