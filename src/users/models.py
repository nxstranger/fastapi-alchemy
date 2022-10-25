from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import deferred, relationship
from sqlalchemy.sql import expression
from ..utils.crypto import hash_password
from src.db import Base


# class Role(Base):
#     __tablename__ = "role_role"
#
#     name = Column(String(50), nullable=False, unique=True)


class User(Base):
    __tablename__ = 'chat_user'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False, unique=True)
    password = deferred(Column(Text, nullable=False))
    active = Column(Boolean, server_default=expression.true(), nullable=False)
    role_name = Column(String(20), nullable=False, server_default='user')

    # sent = relationship('Message')
    # got = relationship('Message')

    def __init__(self, username, password):
        super().__init__()
        hashed_password = hash_password(password)
        self.username = username
        self.password = hashed_password

