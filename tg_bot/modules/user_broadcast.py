from time import sleep
from telegram import TelegramError
from telegram import Update, Bot
from telegram.error import BadRequest
from telegram.ext import Filters, CommandHandler
from telegram.ext.dispatcher import run_async
import tg_bot.modules.sql.userbroadcast_sql as sql
from tg_bot import dispatcher, OWNER_ID, LOGGER


USERS_GROUP = 4
CHAT_GROUP = 10


@run_async
def userbroadcast(bot: Bot, update: Update):
    to_send = update.effective_message.text.split(None, 1)
    if len(to_send) >= 2:
        offset = 0
        batch_size = 10000
        failed = 0
        success = 0
        while True:
            users = sql.get_broadcast_users_batch(offset, batch_size)
            if not users:
                break
            # users = sql.get_all_users() or []
            for user in users:
                try:
                    bot.sendMessage(int(user.user_id), to_send[1])
                    success += 1
                    LOGGER.info("Sent broadcast to %s, username %s, Count: %s", str(
                        user.user_id), str(user.username), str(success))
                    sleep(0.5)
                except TelegramError:
                    sql.del_broadcast_user(user.user_id)
                    failed += 1
                    LOGGER.warning("Deleted ID %s from DB",  str(user.user_id))
                    # LOGGER.warning("Couldn't send broadcast to %s, username %s", str(user.user_id), str(user.username))
            offset = offset + batch_size
            update.effective_message.reply_text(
                "Broadcasting, current status: \n{} users failed\n{} users received".format(failed, success))
        update.effective_message.reply_text(
            "Broadcast complete.\n{} users failed\n{} users received".format(failed, success))


def __stats__():
    return "{} broadcast users".format(sql.num_broadcast_users())


__help__ = ""  # no help string

__mod_name__ = "User_Broadcast"


USER_BROADCAST_HANDLER = CommandHandler(
    "userbroadcast", userbroadcast, filters=Filters.user(OWNER_ID))


dispatcher.add_handler(USER_BROADCAST_HANDLER)
