from sqlalchemy import and_
from ...db.base import current_session
from ...db import Message


def get_user_messages(user_id, receiver_id=None, limit=100, offset=0):
    result = current_session.query(Message)\
        .where(and_(
            (Message.sender_id == user_id),
            (Message.receiver_id == receiver_id) if receiver_id else True
        ))\
        .order_by(Message.id.desc())\
        .limit(limit).offset(offset).all()

    return result


def create_message(user_id, receiver_id, text):
    new_message = Message(
        sender_id=user_id,
        receiver_id=receiver_id,
        text=text,
    )
    current_session.add(new_message)
    try:
        current_session.commit()
        current_session.refresh(new_message)
    except Exception as exc:
        print('ERROR: {}'.format(exc))
        current_session.rollback()

    print("n: {}\nid: {}".format(new_message, new_message.id))
    # new_message_id = Query(Message, session=current_session).add_entity(new_message)
    # current_session.commit()

    return new_message.id
