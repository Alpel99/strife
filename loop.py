import eventlet
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

import pickle
import time
import random

from Gamestate import Gamestate
from Player import Player
from constants import *

# Initialize Flask app and SocketIO
app = Flask(__name__, template_folder='', static_folder='')
socketio = SocketIO(app)

# Define the game loop function
def game_loop():
    global gstate
    while True:
        # Your game logic goes here
        start_time = time.time()
        updateGameState()
        socketio.emit('game_update', gstate.getData(), namespace='/game')
        elapsed_time = time.time() - start_time
        sleep_time = max(0, TICK_INTERVAL - elapsed_time)
        eventlet.sleep(sleep_time)

# Define a route for the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# WebSocket event handler
@socketio.on('connect', namespace='/game')
def game_connect():
    global gstate
    gstate.terrain = gstate.generateTerrain()
    gstate.platforms = gstate.generatePlatforms()
    client_id = request.sid
    # sid = request.namespace.socket.sessid
    print(f'Client {client_id} connected')
    gstate.addPlayer(client_id)
    socketio.emit('game_update', gstate.getData(), namespace='/game')

@socketio.on('disconnect', namespace='/game')
def game_disconnect():
    client_id = request.sid
    gstate.removePlayer(client_id)
    print(f'Client {client_id} disconnected')

@socketio.on('input', namespace='/game')
def player_input(data):
    client_id = request.sid
    global gstate
    gstate.players[client_id].input = data
    # print(f'Client {client_id} event', data)

def updateGameState():
    global gstate
    for p in gstate.players.values():
        p.processInput()
    updatePlayer()

def updatePlayer():
    global gstate
    for p in gstate.players.values():
        if p.id == "test":
            p.state = 1
        movePlayer(p)
        actionPlayer(p)

def movePlayer(p: Player):
    global gstate
    # left/right movement
    if(p.vel[0] > 0 and p.pos[0] < WIDTH or p.vel[0] < 0 and p.pos[0] > 0):
        xstep = min(WIDTH-1, max(0, int(p.pos[0] + p.vel[0])))
        # dont walk over steep terrain, needs jump
        if(p.pos[1] - (HEIGHT-gstate.terrain[xstep]*H_ARR[0]-PLAYER_HEIGHT) <= abs(2*p.vel[0]) or p.jumping):
            p.pos[0] += p.vel[0]
            p.pos[0] = min(WIDTH-1, max(0, p.pos[0]))
    # gravity
    p.pos[1] += p.vel[1]
    # snap to terrain
    t_height = HEIGHT-gstate.terrain[int(p.pos[0])]*H_ARR[0]
    if(p.pos[1] + PLAYER_HEIGHT > t_height):
        p.pos[1] = t_height - PLAYER_HEIGHT
        p.vel[1] = 0
        p.jumping = False
        
def actionPlayer(p):
    global gstate
    # death on low parts of map
    # print(HEIGHT-H_ARR[0]*MIN_HEIGHT - PLAYER_HEIGHT)
    if p.pos[1] == HEIGHT-H_ARR[0]*MIN_HEIGHT - PLAYER_HEIGHT:
        gstate.kill(p.id)
    # hit sides/win
    if not p.side and p.pos[0] == WIDTH-1 or p.side and p.pos[0] == 0:
        gstate.win(p.id)
    if p.state == 3:
        for key in gstate.players.keys():
            if key != p.id:
                res = p.check_hit(gstate.players[key]) 
                if(res is not False):
                    gstate.kill(res)

# Start the game loop in a separate thread
if __name__ == '__main__':
    global gstate
    gstate = Gamestate()
    gstate.addPlayer("test")
    game_thread = eventlet.spawn(game_loop)
    socketio.run(app, host="0.0.0.0", port=8080)