from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from pydantic import BaseModel
from app import models
import random

router = APIRouter()
broadcast_update = None  # gets injected

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Bid(BaseModel):
    game_id: str
    player: str
    amount: float

@router.post("/submit_bid")
def submit_bid(bid: Bid, db: Session = Depends(get_db)):
    player = (
        db.query(models.Player)
        .join(models.Game)
        .filter(models.Game.id == bid.game_id, models.Player.name == bid.player)
        .first()
    )
    if not player:
        return {"error": "Player not found"}

    player.bid = bid.amount
    db.commit()

    # Optional: send update via WebSocket
    return {"status": "bid received"}


@router.post("/create_game")
def create_game(db: Session = Depends(get_db)):
    game_id = str(random.randint(1000, 9999))
    game = models.Game(id=game_id)
    db.add(game)
    db.commit()
    return {"game_id": game_id}


class JoinRequest(BaseModel):
    game_id: str
    player: str

@router.post("/join")
def join_game(req: JoinRequest, db: Session = Depends(get_db)):
    game = db.query(models.Game).filter_by(id=req.game_id).first()
    if not game:
        return {"error": "Game not found"}

    gen = f"G{len(game.players)+1}"
    player = models.Player(name=req.player, generator=gen, game=game)
    db.add(player)
    db.commit()
    return {"generator": gen}