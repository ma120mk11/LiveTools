from sqlalchemy import Column, Integer, String, DateTime, JSON
from app.db.base_class import Base


class Setlist(Base):
    __tablename__ = "setlists"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    