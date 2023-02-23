import os
from importlib import import_module

from NoobStuffs.libformatter import HTML
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import CallbackContext, CommandHandler

from DumprXBot import DEVS, LOGGER, dispatcher, updater
from DumprXBot.helper import CustomFilters
from DumprXBot.modules import ALL_MODULES

for module in ALL_MODULES:
    import_module(f"DumprXBot.modules.{module}")


def start(update: Update, context: CallbackContext):
    user_first_name = update.effective_user.first_name
    bot_first_name = context.bot.first_name
    START_TEXT = ""
    START_TEXT += f"Hey {HTML.bold(f'{user_first_name}')}, I'm {HTML.bold(f'{bot_first_name}')}!\n\n"
    START_TEXT += f"{HTML.bold(f'•')} I'm a bot made to request dumps in {HTML.hyperlink('https://github.com/DumprX/DumprX-CI.git', 'DumprXCI')}.\n"
    START_TEXT += f"{HTML.bold(f'•')} Hit /help to find out more about how to use me to my full potential."
    keyboard = [
        [
            InlineKeyboardButton(text="Channel", url="https://t.me/DumprXDumps"),
            InlineKeyboardButton(text="Support", url="https://t.me/DumprXChat"),
        ],
        [
            InlineKeyboardButton(text="Github", url="https://github.com/DumprX"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.effective_message.reply_html(
        text=START_TEXT,
        reply_markup=reply_markup,
        disable_web_page_preview=True,
    )


def help(update: Update, context: CallbackContext):
    user_id = update.effective_message.from_user.id
    HELP_TEXT = ""
    HELP_TEXT += f"{HTML.bold('Available Commands:')}\n"
    HELP_TEXT += f"- /start: To start me.\n"
    HELP_TEXT += f"- /help: To get this message.\n"
    HELP_TEXT += f"- /dump {{link}}: To request a dump of your file.\n"
    if user_id in DEVS:
        HELP_TEXT += f"- /ping: To check ping of the bot.\n"
        HELP_TEXT += f"- /getcon {{link}}: To get content-type of given link.\n"
        HELP_TEXT += (
            f"- /addcon {{content-type}}: To add content-type to approved formats.\n"
        )
        HELP_TEXT += f"- /rmcon {{content-type}}: To remove content-type from approved formats.\n"
        HELP_TEXT += (
            f"- /cons: To get a list of all the approved content-type formats\n"
        )
        HELP_TEXT += f"- /log: To get a log file of the bot.\n"
        HELP_TEXT += f"- /restart: To restart the bot."
    update.effective_message.reply_html(text=HELP_TEXT)


def main():
    if os.path.isfile(".restartmsg"):
        with open(".restartmsg") as remsg:
            chat_id, msg_id = map(int, remsg)
        dispatcher.bot.edit_message_text(
            text=f"{HTML.bold('Restarted bot successfully!')}",
            chat_id=chat_id,
            message_id=msg_id,
            parse_mode=ParseMode.HTML,
        )
        os.remove(".restartmsg")
    botcmds = [
        ("start", "to start the bot"),
        ("help", "to get help message"),
        ("dump", "to request a dump of your file"),
        ("ping", "to check ping of the bot (dev)"),
        ("getcon", "to get content-type of given link (dev)"),
        ("addcon", "to add content-type to approved formats (dev)"),
        ("rmcon", "to remove content-type from approved formats (dev)"),
        ("cons", "to get a list of all the approved content-type formats (dev)"),
        ("log", "to get a log file of the bot (dev)"),
        ("restart", "to restart the bot (dev)"),
    ]
    dispatcher.bot.set_my_commands(botcmds)
    start_handler = CommandHandler("start", start, filters=CustomFilters.authorized)
    help_handler = CommandHandler("help", help, filters=CustomFilters.authorized)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    LOGGER.info("Using long polling.")
    #    try:
    #        dispatcher.bot.send_message(
    #            chat_id=CHAT_ID,
    #            text=f"{HTML.bold('I am now alive!')}",
    #            parse_mode=ParseMode.HTML,
    #        )
    #    except Unauthorized:
    #        LOGGER.warning("Bot isn't able to send message to priv chat, go and check!")
    #    except BadRequest as e:
    #        LOGGER.warning(e.message)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    LOGGER.info(f"Successfully loaded modules: {str(ALL_MODULES)}")
    main()
