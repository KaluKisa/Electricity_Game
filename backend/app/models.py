from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Game(Base):
    __tablename__ = "games"
    id = Column(String, primary_key=True, index=True)
    round = Column(Integer, default=1)
    players = relationship("Player", back_populates="game")

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    generator = Column(String)
    bid = Column(Float, nullable=True)
    game_id = Column(String, ForeignKey("games.id"))
    game = relationship("Game", back_populates="players")
