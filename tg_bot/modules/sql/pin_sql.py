import threading

from sqlalchemy import Integer, Column, String, func, distinct, Boolean
from sqlalchemy.dialects import postgresql

from tg_bot.modules.sql import SESSION, BASE


class SPinSettings(BASE):
    __tablename__ = "pin_settings"

    chat_id = Column(String(14), primary_key=True)
    message_id = Column(Integer)
    suacpmo = Column(Boolean, default=False)
    scldpmo = Column(Boolean, default=False)

    def __init__(self, chat_id, message_id):
        self.chat_id = str(chat_id)
        self.message_id = message_id


    def __repr__(self):
        return "<Pin Settings for {} in {}>".format(self.chat_id, self.message_id)


SPinSettings.__table__.create(checkfirst=True)

PIN_INSERTION_LOCK = threading.RLock()


def add_mid(chat_id, message_id):
    with PIN_INSERTION_LOCK:
        chat = SESSION.query(SPinSettings).get(str(chat_id))
        if not chat:
            chat = SPinSettings(str(chat_id), message_id)
        SESSION.add(chat)
        SESSION.commit()
        SESSION.close()


def remove_mid(chat_id):
    with PIN_INSERTION_LOCK:
        chat = SESSION.query(SPinSettings).get(str(chat_id))
        if chat:
            SESSION.delete(chat)
            SESSION.commit()
        SESSION.close()


def add_acp_o(chat_id, setting):
    with PIN_INSERTION_LOCK:
        chat = SESSION.query(SPinSettings).get(str(chat_id))
        if not chat:
            chat = SPinSettings(str(chat_id), 0)
        chat.suacpmo = setting
        SESSION.add(chat)
        SESSION.commit()
        SESSION.close()


def add_ldp_m(chat_id, setting):
    with PIN_INSERTION_LOCK:
        chat = SESSION.query(SPinSettings).get(str(chat_id))
        if not chat:
            chat = SPinSettings(str(chat_id), 0)
        chat.scldpmo = setting
        SESSION.add(chat)
        SESSION.commit()
        SESSION.close()


def get_current_settings(chat_id):
    with PIN_INSERTION_LOCK:
        chat = SESSION.query(SPinSettings).get(str(chat_id))
        return chat


