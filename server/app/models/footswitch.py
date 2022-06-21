from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Footswitch(Base):
    __tablename__ = "footswitch"

    id = Column(String(10), primary_key=True)
    name = Column(String)
    is_enabled = Column(Boolean, server_default='true', default=True)
    description = Column(String)
    buttons = relationship(
        "Button",
        cascade="all,delete,delete-orphan",
        order_by="Button.id",
        back_populates="footswitch",
    )

    def __repr__(self):
        return f"<Footswitch '{self.name}' ({self.id})>"

class Button(Base):
    __tablename__ = "fs_buttons"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    name = Column(String)
    has_led = Column(Boolean, server_default='false', default=False)
    action_cat = Column(String)
    action_id = Column(String)
    fs_id = Column(String(10), ForeignKey("footswitch.id"))
    footswitch = relationship("Footswitch", back_populates="buttons")