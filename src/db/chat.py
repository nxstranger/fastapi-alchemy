import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


class Message(Base):
    __tablename__ = "chat_message"

    id = sa.Column(sa.Integer, primary_key=True)
    sender_id = sa.Column(sa.Integer, sa.ForeignKey("chat_user.id"), nullable=False)
    receiver_id = sa.Column(sa.Integer, sa.ForeignKey("chat_user.id"), nullable=False)
    text = sa.Column(sa.Text, nullable=False)
    created_at = sa.Column(sa.TIMESTAMP, server_default=func.now())

    sender = relationship(
        "User",
        foreign_keys=[sender_id],
        uselist=False,
    )
    receiver = relationship(
        "User",
        foreign_keys=[receiver_id],
        uselist=False,
    )
