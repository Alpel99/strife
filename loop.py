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
    while True:
        # Your game logic goes here
        # This is a simple example that emits a random number to all connected clients
        import random
        number = random.randint(1, 100)
        socketio.emit('game_update', {'number': number}, namespace='/game')
        eventlet.sleep(1)  # Adjust the sleep time as needed

# Define a route for the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# WebSocket event handler
@socketio.on('connect', namespace='/game')
def game_connect():
    sid = request.sid
    # sid = request.namespace.socket.sessid
    print(f'Client {sid} connected')

@socketio.on('disconnect', namespace='/game')
def game_disconnect():
    sid = request.sid
    # sid = request.namespace.socket.sessid
    print(f'Client {sid} disconnected')

@socketio.on('input', namespace='/game')
def player_input(data):
    print('Client event', data)

# Start the game loop in a separate thread
if __name__ == '__main__':
    global gstate
    gstate = Gamestate()
    game_thread = eventlet.spawn(game_loop)
    socketio.run(app, host="localhost", port=8080)