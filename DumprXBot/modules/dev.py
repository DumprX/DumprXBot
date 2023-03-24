import time
from os import execl
from sys import executable

from NoobStuffs.libformatter import HTML
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, CommandHandler

from DumprXBot import CONFIGS, LOGGER, StartTime, dispatcher
from DumprXBot.helper import CustomFilters, DbManager, dev_check, get_readable_time


@dev_check
def ping(update: Update, context: CallbackContext):
    start_time = time.time()
    message = update.effective_message.reply_html(f"{HTML.mono('Pinging...')}")
    end_time = time.time()
    telegram_ping = f"{str(round((end_time - start_time) * 1000, 3))} ms"
    uptime = get_readable_time(time.time() - StartTime)
    PING_TEXT = ""
    PING_TEXT += f"PONG!!\n"
    PING_TEXT += f"{HTML.bold('Time Taken:')} {HTML.mono(f'{telegram_ping}')}\n"
    PING_TEXT += f"{HTML.bold('Service Uptime:')} {HTML.mono(f'{uptime}')}"
    message.edit_text(
        text=PING_TEXT,
        parse_mode=ParseMode.HTML,
    )


@dev_check
def send_log(update: Update, context: CallbackContext):
    with open(f"DumprXBot.log", "rb") as log:
        update.effective_message.reply_document(
            document=log,
            filename=log.name,
            parse_mode=ParseMode.HTML,
        )


@dev_check
def maintenance(update: Update, context: CallbackContext):
    args = context.args
    if not args or len(args) > 1:
        TEXT = f"{HTML.bold('Usage:')} {HTML.mono('/maintenance {ON/OFF}')}"
        return update.effective_message.reply_html(text=TEXT)
    arg = args[0].lower()
    status = CONFIGS["in_maintenance"]
    if arg == "on" and status == True:
        TEXT = f"{HTML.bold('Bot is already on maintenance mode.')}"
    elif arg == "on" and status == False:
        CONFIGS["in_maintenance"] = True
        DbManager().toggleconf("in_maintenance", True)
        TEXT = f"{HTML.bold('Turned on maintenance mode.')}"
    elif arg == "off" and status == True:
        CONFIGS["in_maintenance"] = False
        DbManager().toggleconf("in_maintenance", False)
        TEXT = f"{HTML.bold('Turned off maintenance mode.')}"
    elif arg == "off" and status == False:
        TEXT = f"{HTML.bold('Bot is not on maintenance mode.')}"
    else:
        TEXT = f"{HTML.bold('Usage:')} {HTML.mono('/maintenance {ON/OFF}')}"
        return update.effective_message.reply_html(text=TEXT)
    update.effective_message.reply_html(text=TEXT)


@dev_check
def restart(update: Update, context: CallbackContext):
    restart_message = update.effective_message.reply_html(
        text=f"{HTML.mono('Restarting bot...')}",
    )
    LOGGER.info("Restarting bot...")
    with open(".restartmsg", "w") as remsg:
        remsg.truncate(0)
        remsg.write(f"{restart_message.chat_id}\n{restart_message.message_id}\n")
    execl(executable, executable, "-m", "DumprXBot")


ping_handler = CommandHandler("ping", ping, filters=CustomFilters.authorized)
log_handler = CommandHandler("log", send_log, filters=CustomFilters.authorized)
maintenance_handler = CommandHandler(
    "maintenance",
    maintenance,
    filters=CustomFilters.authorized,
)
restart_handler = CommandHandler("restart", restart, filters=CustomFilters.authorized)
dispatcher.add_handler(ping_handler)
dispatcher.add_handler(log_handler)
dispatcher.add_handler(maintenance_handler)
dispatcher.add_handler(restart_handler)
