from NoobStuffs.libformatter import HTML
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from DumprXBot import dispatcher
from DumprXBot.helper import CustomFilters, get_direct_link


def direct_link(update: Update, context: CallbackContext):
    args = context.args
    if not args or len(args) > 1:
        TEXT = f"{HTML.bold('Usage:')} {HTML.mono('/direct {link}')}"
        return update.effective_message.reply_html(text=TEXT)
    link = args[0]
    res = get_direct_link(link)
    if res:
        TEXT = f"{HTML.bold('Direct Link:')} {HTML.mono(f'{res}')}"
    else:
        TEXT = f"{HTML.bold('Direct Link:')} {HTML.mono(f'Invalid URL')}"
    update.effective_message.reply_html(text=TEXT)


direct_link_handler = CommandHandler(
    "direct",
    direct_link,
    filters=CustomFilters.authorized,
)
dispatcher.add_handler(direct_link_handler)
