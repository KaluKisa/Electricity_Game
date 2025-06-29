from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.routers import game
from app.database import Base, engine

app = FastAPI()
Base.metadata.create_all(bind=engine)
clients = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(game.router)

@app.websocket("/ws/{game_id}/{player}")
async def websocket_endpoint(websocket: WebSocket, game_id: str, player: str):
    await websocket.accept()
    if game_id not in clients:
        clients[game_id] = {}
    clients[game_id][player] = websocket

    try:
        while True:
            await websocket.receive_text()  # no-op
    except WebSocketDisconnect:
        del clients[game_id][player]

# Broadcast function to call from game logic
async def broadcast_update(game_id: str, game_state: dict):
    for ws in clients.get(game_id, {}).values():
        await ws.send_json(game_state)


# Inject into router
game.broadcast_update = broadcast_update
