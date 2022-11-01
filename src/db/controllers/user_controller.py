from sqlalchemy.exc import IntegrityError

from ..user import User
from ..base import current_session


async def get_user_by_username(username):
    user = current_session.query(User)\
        .filter(User.username == username).first()
    return user


async def create_new_user(credentials):
    new_user = User(**credentials)
    current_session.add(new_user)
    try:
        current_session.commit()
    except IntegrityError:
        current_session.rollback()
        return None
    current_session.refresh(new_user)
    return new_user


async def update_user_data(user_id, values):
    try:
        update_result = current_session.query(User)\
            .filter(User.id == user_id)\
            .update(values, synchronize_session='fetch')
        current_session.commit()
        return update_result
    except Exception as exc:
        print('ERROR update_user_data: {}'.format(exc))
        current_session.rollback()
    return None

