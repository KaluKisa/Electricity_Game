from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import SessionLocal
from app import models
import random

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_game_state(game_id: str, db: Session):
    game = db.query(models.Game).filter_by(id=game_id).first()
    if not game:
        return {}
    return {
        "game_id": game.id,
        "round": game.round,
        "players": [
            {"name": p.name, "generator": p.generator, "bid": p.bid}
            for p in game.players
        ]
    }


class JoinRequest(BaseModel):
    game_id: str
    player: str

class Bid(BaseModel):
    game_id: str
    player: str
    amount: float


@router.post("/create_game")
def create_game(db: Session = Depends(get_db)):
    game_id = str(random.randint(1000, 9999))
    game = models.Game(id=game_id)
    db.add(game)
    db.commit()
    return {"game_id": game_id}


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


@router.post("/submit_bid")
async def submit_bid(bid: Bid, db: Session = Depends(get_db)):
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

    from app.main import clients  # circular import workaround
    if bid.game_id in clients:
        state = get_game_state(bid.game_id, db)
        for ws in clients[bid.game_id].values():
            await ws.send_json(state)

    return {"status": "bid received"}