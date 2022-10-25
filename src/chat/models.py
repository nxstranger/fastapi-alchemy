from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text,
)
from sqlalchemy.orm import relationship
from src.db import Base
# from ..users.models import User


class Message(Base):
    __tablename__ = "chat_message"

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey("chat_user.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("chat_user.id"), nullable=False)
    text = Column(Text, nullable=False)

    sender = relationship(
        "User",
        # back_populates="sent",
        foreign_keys=[sender_id],
        uselist=False,
    )
    receiver = relationship(
        "User",
        # back_populates="got",
        foreign_keys=[receiver_id],
        uselist=False,
    )
