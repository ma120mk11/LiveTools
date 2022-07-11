from sqlalchemy import Column, Integer, String, DateTime, JSON, func
from app.db.base_class import Base


class Setlist(Base):
    __tablename__ = "setlists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    comments = Column(String)
    created = Column(DateTime, server_default=func.now())
    tags = Column(String)
    setup = Column(String)
    last_played = Column(DateTime, server_default=func.now())
    actions = Column(JSON)