from NoobStuffs.libformatter import HTML
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Message, ParseMode
from telegram.ext import MessageFilter

from DumprXBot import (
    CHAT_IDS,
    CONFIGS,
    DEVS,
    MAINTENANCE_USER_ENCOUNTER,
    UNAUTHORIZED_CHATS_ENCOUTER,
    dispatcher,
    updater,
)


def check_maintenance(usr_id_check: int, chat_id: int, msg_id: int):
    if CONFIGS["in_maintenance"]:
        if usr_id_check not in DEVS:
            if usr_id_check in MAINTENANCE_USER_ENCOUNTER:
                return False
            else:
                updater.bot.send_message(
                    text=f"{HTML.bold('Bot is under maintenance.')}",
                    chat_id=chat_id,
                    reply_to_message_id=msg_id,
                    parse_mode=ParseMode.HTML,
                )
                MAINTENANCE_USER_ENCOUNTER.append(usr_id_check)
                return False
    return True


class CustomFilters:
    class Authorized(MessageFilter):
        def filter(self, message: Message):
            if message.chat.type != "private":
                if (
                    message.from_user.id not in DEVS
                    and message.chat.id in UNAUTHORIZED_CHATS_ENCOUTER
                ):
                    return False
                if message.from_user.id not in DEVS and message.chat.id not in CHAT_IDS:
                    TEXT = f"Hello, {message.from_user.first_name}!, I'm group restricted.\nPlease join support group and use me there."
                    keyboard = [
                        [
                            InlineKeyboardButton(
                                text="Support",
                                url="https://t.me/DumprXChat",
                            ),
                            InlineKeyboardButton(
                                text="Channel",
                                url="https://t.me/DumprXDumps",
                            ),
                        ],
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    message.reply_html(
                        text=TEXT,
                        reply_markup=reply_markup,
                    )
                    dispatcher.bot.leave_chat(message.chat.id)
                    UNAUTHORIZED_CHATS_ENCOUTER.append(message.chat.id)
                    return False
                else:
                    return check_maintenance(
                        message.from_user.id,
                        message.chat.id,
                        message.message_id,
                    )
            else:
                if (
                    message.from_user.id not in DEVS
                    and message.from_user.id in UNAUTHORIZED_CHATS_ENCOUTER
                ):
                    return False
                if message.from_user.id not in DEVS:
                    TEXT = f"Hello, {message.from_user.first_name}!\nPlease join support group and use me there."
                    keyboard = [
                        [
                            InlineKeyboardButton(
                                text="Support",
                                url="https://t.me/DumprXChat",
                            ),
                            InlineKeyboardButton(
                                text="Channel",
                                url="https://t.me/DumprXDumps",
                            ),
                        ],
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    message.reply_html(
                        text=TEXT,
                        reply_markup=reply_markup,
                    )
                    UNAUTHORIZED_CHATS_ENCOUTER.append(message.from_user.id)
                    return False
                else:
                    return check_maintenance(
                        message.from_user.id,
                        message.chat.id,
                        message.message_id,
                    )

    authorized = Authorized()
