from fastapi import APIRouter
from pydantic import BaseModel
import random
from typing import Optional

router = APIRouter()
games = {}
broadcast_update = None  # gets injected

class Bid(BaseModel):
    game_id: str
    player: str
    amount: float

@router.post("/submit_bid")
async def submit_bid(bid: Bid):
    game = games[bid.game_id]
    game["players"][bid.player]["bid"] = bid.amount
    if broadcast_update:
        await broadcast_update(bid.game_id, game)
    return {"status": "bid received"}


@router.post("/create_game")
def create_game():
    game_id = str(random.randint(1000, 9999))
    games[game_id] = {"players": {}, "round": 1}
    return {"game_id": game_id}

@router.post("/join")
def join_game(game_id: str, player: str):
    if game_id not in games:
        return {"error": "Game not found"}
    games[game_id]["players"][player] = {
        "bid": None,
        "generator": f"G{len(games[game_id]['players'])+1}"
    }
    return games[game_id]["players"][player]
