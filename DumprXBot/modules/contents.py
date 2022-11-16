from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from DumprXBot import CONTENT_FORMATS, DB_URL, dispatcher
from DumprXBot.helper import (
    CustomFilters,
    DbManager,
    bold,
    dev_check,
    get_content_type,
    mono,
)


@dev_check
def get_con(update: Update, context: CallbackContext):
    args = context.args
    if not args or len(args) > 1:
        TEXT = f"{bold('Usage:')} {mono('/getcon {link}')}"
        update.effective_message.reply_html(text=TEXT)
        return
    link = args[0]
    contype = get_content_type(link)
    TEXT = f"{bold('Content Type:')} {mono(f'{contype}')}"
    update.effective_message.reply_html(text=TEXT)


@dev_check
def add_con(update: Update, context: CallbackContext):
    args = context.args
    if not args or len(args) > 1:
        TEXT = f"{bold('Usage:')} {mono('/addcon {content-type}')}"
        update.effective_message.reply_html(text=TEXT)
        return
    con = args[0]
    if con in CONTENT_FORMATS:
        TEXT = f"{con} is already a {bold('Content formats!')}"
        update.effective_message.reply_html(text=TEXT)
        return
    if DB_URL is not None:
        TEXT = DbManager().addcon(con)
    else:
        TEXT = f"Successfully added {mono(f'{con}')} to {bold('Content formats!')}"
    CONTENT_FORMATS.append(con)
    update.effective_message.reply_html(text=TEXT)


@dev_check
def rm_con(update: Update, context: CallbackContext):
    args = context.args
    if not args or len(args) > 1:
        TEXT = f"{bold('Usage:')} {mono('/rmcon {content-type}')}"
        update.effective_message.reply_html(text=TEXT)
        return
    con = args[0]
    if con not in CONTENT_FORMATS:
        TEXT = f"{con} is not in {bold('Content formats!')}"
        update.effective_message.reply_html(text=TEXT)
        return
    if DB_URL is not None:
        TEXT = DbManager().rmcon(con)
    else:
        TEXT = f"Successfully removed {mono(f'{con}')} from {bold('Content formats!')}"
    CONTENT_FORMATS.remove(con)
    update.effective_message.reply_html(text=TEXT)


@dev_check
def all_cons(update: Update, context: CallbackContext):
    TEXT = ""
    TEXT += f"{bold('Content Formats:')}\n"
    if len(CONTENT_FORMATS) == 0:
        TEXT += f"{mono('None')}\n"
    else:
        for ctypes in CONTENT_FORMATS:
            TEXT += f"{mono(f'{ctypes}')}\n"
    update.effective_message.reply_html(text=TEXT)


getcon_handler = CommandHandler("getcon", get_con, filters=CustomFilters.authorized)
addcon_handler = CommandHandler("addcon", add_con, filters=CustomFilters.authorized)
rmcon_handler = CommandHandler("rmcon", rm_con, filters=CustomFilters.authorized)
allcons_handler = CommandHandler("cons", all_cons, filters=CustomFilters.authorized)

dispatcher.add_handler(getcon_handler)
dispatcher.add_handler(addcon_handler)
dispatcher.add_handler(rmcon_handler)
dispatcher.add_handler(allcons_handler)
