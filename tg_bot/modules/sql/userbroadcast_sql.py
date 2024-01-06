import threading
from sqlalchemy import Column, BigInteger, UnicodeText, ForeignKey, UniqueConstraint, func
from tg_bot.modules.sql import BASE, SESSION


class Broadcast(BASE):
    __tablename__ = "broadcast"
    user_id = Column(BigInteger, primary_key=True)
    username = Column(UnicodeText)

    def __init__(self, user_id, username=None):
        self.user_id = user_id
        self.username = username

    def __repr__(self):
        return "<User {} ({})>".format(self.username, self.user_id)


Broadcast.__table__.create(bind=SESSION.get_bind(), checkfirst=True)

INSERTION_LOCK = threading.RLock()


def update_broadcast_user(user_id, username):
    with INSERTION_LOCK:
        user = SESSION.query(Broadcast).get(user_id)
        if not user:
            user = Broadcast(user_id, username)
            SESSION.add(user)
            SESSION.flush()
        else:
            user.username = username

        SESSION.commit()


def get_broadcast_users():
    try:
        return SESSION.query(Broadcast).all()
    finally:
        SESSION.close()


def get_broadcast_users_batch(offset, batch_size):
    try:
        return SESSION.query(Broadcast).offset(offset).limit(batch_size).all()
    finally:
        SESSION.close()


def del_broadcast_user(user_id):
    with INSERTION_LOCK:
        curr = SESSION.query(Broadcast).get(user_id)
        if curr:
            SESSION.delete(curr)
            SESSION.commit()
            return True

        SESSION.close()
    return False


def num_broadcast_users():
    try:
        return SESSION.query(Broadcast).count()
    finally:
        SESSION.close()
