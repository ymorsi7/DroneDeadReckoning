from fastapi import FastAPI, WebSocket, Request, Response    # The main FastAPI import and Request/Response objects
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse    # Used to redirect to another route
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel     
from flask import Flask, request, render_template
from flask_socketio import SocketIO
from rktellolib import Tello
import uvicorn
import asyncio
import plotly.graph_objects as go
import json
import numpy as np
import time

app = FastAPI()
theSocket = Flask(__name__)
socketio = SocketIO(theSocket)
app.mount("/assets", StaticFiles(directory="assets"), name="assets")


@app.get("/", response_class=HTMLResponse)
def get_html() -> HTMLResponse:
    with open("index.html") as html:
        return HTMLResponse(content=html.read())


@app.get("/main.js", response_class=HTMLResponse)
def get_js() -> HTMLResponse:
    with open("main.js") as js:
        return HTMLResponse(content=js.read(), media_type="application/javascript")

tello = Tello(debug=False, has_video=False)
tello.connect()

@app.websocket("/ws")
async def websocketEndpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        command = await websocket.receive_text()
        await processCommand(command)

@app.websocket("/wsPosition")
async def websocketPositionEndpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        droneState = getDroneState()
        await websocket.send_json(droneState)
        await asyncio.sleep(0.1)

async def processCommand(command):
    if command == 'takeoff':
        tello.takeoff()
    elif command == 'land':
        tello.land()
    elif command == 'left':
        tello.left(30)
    elif command == 'right':
        tello.right(30)
    elif command == 'forward':
        tello.forward(30)
    elif command == 'backward':
        tello.back(30)
    elif command == 'up':
        tello.up(30)
    elif command == 'down':
        tello.down(30)
    elif command == 'rotateCW':
        tello.cw(360)
    elif command == 'rotateCCW':
        print("hicC")
        tello.ccw(360)



# Create a figure to hold the trajectory plot
fig = go.Figure()



@app.websocket("/ws_position")
async def websocket_position_endpoint(websocket: WebSocket):
    await websocket.accept()
    # Initialize the drone position
    t = np.zeros(1)
    x = np.zeros(1)
    y = np.zeros(1)
    z = np.zeros(1)
    start_time = time.time()
    i = 0
    while True:
        current_time = time.time()
        delta_t = (current_time - start_time) - t[i]
        t = np.append(t,float(current_time - start_time))
        x = np.append(x,x[i] + delta_t*float(tello.get_vx()))
        y = np.append(y,y[i] + delta_t*float(tello.get_vy()))
        z = np.append(z,z[i] + delta_t*float(tello.get_vz()))
        i += 1
        drone_state = {
            "x": x[i],
            "y": y[i],
            "z": (-1) * z[i]
        }
        jsonObj = json.dumps(drone_state)

        await websocket.send_json(jsonObj)
        await asyncio.sleep(0.1)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6543)
