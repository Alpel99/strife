import eventlet
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

import json
import pickle
import time

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
    gstate.generateTerrain()
    client_id = request.sid
    # sid = request.namespace.socket.sessid
    print(f'Client {client_id} connected')
    gstate.players[client_id] = Player(client_id)
    socketio.emit('game_update', gstate.getData(), namespace='/game')

@socketio.on('disconnect', namespace='/game')
def game_disconnect():
    client_id = request.sid
    del gstate.players[client_id]
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
    playerAction()

def playerAction():
    global gstate
    for p in gstate.players.values():
        movePlayer(p)
        actionPlayer(p)

def movePlayer(p: Player):
    if(p.vel[0] > 0 and p.pos[0] < WIDTH or p.vel[0] < 0 and p.pos[0] > 0):
        p.pos[0] += p.vel[0]
        p.pos[0] = min(1920, max(0, p.pos[0]))
    p.pos[1] += p.vel[1]
    t_height = HEIGHT-gstate.terrain[min(int(p.pos[0]), 1919)]*H_ARR[0]
    if(p.pos[1] + PLAYER_HEIGHT > t_height):
        p.pos[1] = t_height - PLAYER_HEIGHT
        p.vel[1] = 0
        p.jumping = False
        
def actionPlayer(p):
    if p.pos[1] == HEIGHT-H_ARR[0]*MIN_HEIGHT - PLAYER_HEIGHT:
        p.death()

# Start the game loop in a separate thread
if __name__ == '__main__':
    global gstate
    gstate = Gamestate()
    game_thread = eventlet.spawn(game_loop)
    socketio.run(app, host="localhost", port=8080)