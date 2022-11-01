from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    ForeignKey,
)
import enum
from sqlalchemy.orm import deferred
from sqlalchemy.sql import expression
from src.utils.crypto import hash_password
from .base import Base


class RoleEnum(enum.Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class User(Base):
    __tablename__ = 'chat_user'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False, unique=True)
    password = deferred(Column(Text, nullable=False))
    is_active = Column(Boolean, server_default=expression.true(), nullable=False)
    role_name = Column(String(10),
                       nullable=False,
                       server_default=RoleEnum.USER.value)
    contact_id = Column(Integer, ForeignKey("chat_user.id"))

    def __init__(self, username, password, role_name=RoleEnum.USER.value):
        super().__init__()
        hashed_password = hash_password(password)
        self.username = username
        self.password = hashed_password
        self.role_name = role_name
