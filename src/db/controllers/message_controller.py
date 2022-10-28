from sqlalchemy import and_
from src.db.base import current_session
from src.db import Message


def get_user_messages(user_id, receiver_id=None, limit=100, offset=0):
    result = current_session.query(Message)\
        .where(and_(
            (Message.sender_id == user_id),
            (Message.receiver_id == receiver_id) if receiver_id else True
        ))\
        .order_by(Message.id.desc())\
        .limit(limit).offset(offset).all()

    return result


async def create_message(user_id, receiver_id, text):
    new_message = Message(
        sender_id=user_id,
        receiver_id=receiver_id,
        text=text,
    )
    current_session.add(new_message)
    try:
        current_session.commit()
    except Exception as exc:
        print('ERROR: {}'.format(exc))
        current_session.rollback()
        return None

    current_session.refresh(new_message)
    return new_message.id
