import http.server
import asyncio
import websockets
from websockets.server import serve
import threading
import json
import pickle
import time

from Gamestate import Gamestate
from Player import Player
from constants import *

class MyHTTPServer(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        # remove sometime later
        updateSource()
        global page
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(page.encode("utf-8"))

def updateSource():
    global page
    html_file = open("index.html", "r")
    html = html_file.read()
    html_file.close()

    js_file = open("script.js", "r")
    js = js_file.read()
    js_file.close()

    p5_file = open("p5.min.js", "r")
    p5 = p5_file.read()
    p5_file.close()
    page = html + "<script>" + js + "</script>" + "<script>" + p5 + "</script>"

def start_http_server():
    http_server = http.server.HTTPServer(("", 8080), MyHTTPServer)
    http_server.serve_forever()

def websocket_server_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(websockets.serve(handle_websocket, "localhost", 8000))
    loop.run_forever()

async def handle_websocket(websocket, path):
    try:
        client_id = id(websocket)
        global gstate
        gs = gstate.getJSON()
        await websocket.send(gs)
        while True:
            message = await websocket.recv()
            try:
                data = json.loads(message)
                await process_message(data, websocket)
            except json.JSONDecodeError as e:
                print("JSON decoding error:", e)
                print("Received data:", message)
                # Handle the error gracefully, if necessary
    except (websockets.exceptions.ConnectionClosedError, websockets.exceptions.ConnectionClosedOK) as e:
        print("Websocket connection closed")
        del gstate.players[client_id]
        # Handle connection closed

async def process_message(data, websocket):
    client_id = id(websocket)
    # print(data)
    # m = {"id": -1}
    match data["id"]:
        # new connection
        case -1:
            print(client_id)
            gstate.players[client_id] = Player(client_id)
            gs = gstate.getData()
            await websocket.send(gs)
        case 0:
            pass # used to send gamestate
        case 1:
            # input keys for player
            processPlayerInput(data, client_id)
        case _:
            print("Wrong message id: ", data)
    
def processPlayerInput(data, client_id):
    global gstate
    p = gstate.players[client_id]
    if(data["right"] == 1 and p.vel[0] < MAX_VELOCITY):
        p.vel[0] = p.vel[0] + X_ACCELERATION
    if(data["left"] == 1 and p.vel[0] > -MAX_VELOCITY):
        p.vel[0] = p.vel[0] - X_ACCELERATION

# def game_loop():
#     global message_queue
#     while True:
#         start_time = time.time()  # Record the start time of the iteration
#         gameLogic()
#         gs = gstate.getJSON()
#         # print("send", gs)
#         message_queue.put_nowait(gs)
#         elapsed_time = time.time() - start_time
#         if elapsed_time < FRAME_TIME:
#             time.sleep(FRAME_TIME - elapsed_time)

def game_loop():
    loop = asyncio.new_event_loop()  # Create a new event loop for the game loop
    asyncio.set_event_loop(loop)

    async def game_loop_coroutine():
        global gstate
        async with websockets.connect("ws://localhost:8000") as websocket:
            while True:
                start_time = time.time()
                gameLogic()
                gs = gstate.getJSON()
                
                try:
                    await websocket.send(gs)  # Send data to the websocket
                except websockets.exceptions.ConnectionClosed:
                    print("WebSocket connection closed")
                    break  # Break the loop if the connection is closed
                
                elapsed_time = time.time() - start_time
                if elapsed_time < FRAME_TIME:
                    await asyncio.sleep(FRAME_TIME - elapsed_time)  # Use "await" for sleeping

    loop.run_until_complete(game_loop_coroutine())

def gameLogic():
    global gstate
    for p in gstate.players.values():
        if(p.vel[0] > 0 and p.position[0] < WIDTH or p.vel[0] < 0 and p.position[0] > 0):
            p.position[0] += p.vel[0]
            p.position[0] = min(1920, max(0, p.position[0]))
        if(p.vel[1] > 0):
            p.position[1] += p.vel[1]
        else:
            # simple drop
            if(p.position[1] > gstate.terrain[int(p.position[0])]*H_ARR[0]):
                p.position[1] += p.vel[1]
    for p in gstate.players.values():
        print(p.position)


async def main():
    updateSource()

    loop = asyncio.get_event_loop()

    http_thread = threading.Thread(target=start_http_server, daemon=True)
    http_thread.start() 
    
    websocket_thread = threading.Thread(target=websocket_server_thread, daemon=True)
    websocket_thread.start()
    # websocket_server = await websockets.serve(handle_websocket, "localhost", 8000)
    
    game_thread = threading.Thread(target=game_loop, daemon=True)
    game_thread.start()

    try:
        while True:
            await asyncio.sleep(1)  # Keep the main thread running
    finally:
        # Cleanup and stop the loop if needed
        loop.stop()

if __name__ == "__main__":
    global gstate
    gstate = Gamestate()
    # f = open('gstate.pkl', 'wb')
    # gstate = pickle.load(f)
    message_queue = asyncio.Queue()
    asyncio.run(main())
