from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegram.ext import MessageFilter

from DumprXBot import CHAT_IDS, DEVS, UNAUTHORIZED_CHATS_ENCOUTER, dispatcher


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
                    return True
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
                    return True

    authorized = Authorized()
