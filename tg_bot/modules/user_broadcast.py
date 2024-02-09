import time
import datetime
from time import sleep
from telegram import TelegramError
from telegram import Update, Bot
from telegram import ParseMode
from telegram.error import BadRequest, Unauthorized
from telegram.ext import Filters, CommandHandler
from telegram.ext.dispatcher import run_async
import tg_bot.modules.sql.userbroadcast_sql as sql
from tg_bot import dispatcher, OWNER_ID, LOGGER


USERS_GROUP = 4
CHAT_GROUP = 10


@run_async
def userbroadcast(bot: Bot, update: Update):
    to_send = update.effective_message.text.split(None, 1)
    from_id = update.effective_message.chat.id
    if len(to_send) >= 2:
        bot.sendMessage(
            int(from_id),
            "Starting broadcast...\nContent:\n\n" + to_send[1],
            parse_mode=ParseMode.MARKDOWN,
        )
        failed = 0
        success = 0
        # offset = 0
        # batch_size = 10000
        # while True:
        #     users = sql.get_broadcast_users_batch(offset, batch_size)
        #     if not users:
        #         break
        start_time = time.time()
        users = sql.get_broadcast_users() or []
        for user in users:
            try:
                bot.sendMessage(
                    int(user.user_id), to_send[1], parse_mode=ParseMode.MARKDOWN
                )
                success += 1
                LOGGER.info(
                    "Sent broadcast to %s, username %s, Count: %s",
                    str(user.user_id),
                    str(user.username),
                    str(success),
                )
                sleep(0.5)
            except TelegramError as e:
                failed += 1
                LOGGER.warning(
                    "Failed to send broadcast to %s, Count: %s, Error: %s",
                    str(user.user_id),
                    str(failed),
                    str(e),
                )
                # LOGGER.warning("Couldn't send broadcast to %s, username %s", str(user.user_id), str(user.username))
            # offset = offset + batch_size
            # update.effective_message.reply_text(
            #     f"Broadcasting, current status: \n{failed} users failed\n{success} users received\nTotal completed: {offset}")
        time_taken = datetime.timedelta(seconds=int(time.time() - start_time))
        update.effective_message.reply_text(
            f"Broadcast complete.\n{failed} users failed\n{success} users\nCompleted in {time_taken} HH:MM:SS"
        )


@run_async
def user_stats(bot: Bot, update: Update):
    stopped_users, active_users = 0, 0
    users = sql.get_broadcast_users()
    LOGGER.info("Starting active users check...")
    update.effective_message.reply_text(
        f"Found {len(users)} users in DB.\nStarting active users check..."
    )
    start_time = time.time()

    for user in users:
        cid = user.user_id
        sleep(0.1)

        try:
            bot.send_chat_action(cid, "TYPING", timeout=120)
            LOGGER.info("Active user %s", str(cid))
            active_users += 1
            sleep(0.1)
        except (BadRequest, Unauthorized) as e:
            LOGGER.warning("Deleted ID %s from DB, Error: %s", str(cid), str(e))
            stopped_users += 1
            sql.del_broadcast_user(cid)
            sleep(0.1)
    time_taken = datetime.timedelta(seconds=int(time.time() - start_time))
    update.effective_message.reply_text(
        f"Usercheck complete.\n{active_users} users active\n{stopped_users} users stopped\nCompleted in {time_taken} HH:MM:SS"
    )


def __stats__():
    return f"{sql.num_broadcast_users()} broadcast users"


__help__ = ""  # no help string

__mod_name__ = "User_Broadcast"


USER_BROADCAST_HANDLER = CommandHandler(
    "userbroadcast", userbroadcast, filters=Filters.user(OWNER_ID)
)
USER_STATS_HANDLER = CommandHandler(
    "userstats", user_stats, filters=Filters.user(OWNER_ID)
)

dispatcher.add_handler(USER_BROADCAST_HANDLER)
dispatcher.add_handler(USER_STATS_HANDLER)
