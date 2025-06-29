from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.database import Base, engine
from app.routers import game
from app.routers.game import get_game_state, get_db
from sqlalchemy.orm import Session

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(game.router)

clients = {}

@app.websocket("/ws/{game_id}/{player}")
async def websocket_endpoint(websocket: WebSocket, game_id: str, player: str):
    await websocket.accept()
    if game_id not in clients:
        clients[game_id] = {}
    clients[game_id][player] = websocket
    try:
        while True:
            await websocket.receive_text()  # Keep alive
    except WebSocketDisconnect:
        del clients[game_id][player]