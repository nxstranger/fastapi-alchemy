from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Text
)
from ..utils.crypto import hash_password
from sqlalchemy.orm import relationship
from src.db import Base
# from ..chat.models import Message


class User(Base):
    __tablename__ = "chat_user"

    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False, unique=True)
    password = Column(Text, nullable=False)

    # sent = relationship("Message", back_populates="sender")
    # got = relationship("Message", back_populates="receiver")

    def __init__(self, username, password):
        super().__init__()
        print('U:{}\nP:{}'.format(username, password))
        hashed_password = hash_password(password)
        self.username = username
        self.password = hashed_password

