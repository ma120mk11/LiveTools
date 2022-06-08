from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, ForeignKey

from app.db.base_class import Base

class LightCommand(Base):
    __tablename__ = "osc_light"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    osc_path = Column(String)
    type = Column(String)
    auto_release_ms = Column(Integer)
    category = Column(Integer)
