from NoobStuffs.libformatter import HTML
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import CallbackContext, CommandHandler

from DumprXBot import PR_REPO, dispatcher
from DumprXBot.helper import CustomFilters, GithubHandler, check_link


def dump(update: Update, context: CallbackContext):
    args = context.args
    if not args or len(args) > 1:
        TEXT = f"{HTML.bold('Usage:')} {HTML.mono('/dump {link}')}"
        update.effective_message.reply_html(text=TEXT)
        return
    link = args[0]
    msg = update.effective_message.reply_html(
        f"{HTML.mono('Checking request link...')}",
    )
    if not check_link(link):
        TEXT = f"Please give any valid download link"
        msg.edit_text(text=TEXT, parse_mode=ParseMode.HTML)
        return
    msg.edit_text(
        text=f"{HTML.mono('Making pull request...')}",
        parse_mode=ParseMode.HTML,
    )
    user_id = update.effective_message.from_user.id
    full_name = update.effective_message.from_user.full_name
    username = update.effective_message.from_user.username or None
    USER_INFO = ""
    if username is not None:
        USER_INFO += f"User: [{full_name}](https://t.me/{username})\n"
    else:
        USER_INFO += f"User: {full_name}\n"
    USER_INFO += f"User ID: {user_id}\n"
    USER_INFO += f"Request Link: {link}"
    pull = GithubHandler.make_pr(link, USER_INFO)
    msg.delete()
    TEXT = "#DUMP_REQ\n"
    TEXT += f"{HTML.bold('Your dump request is successful!')}\n"
    if username is not None:
        TEXT += f"{HTML.bold('User:')} {HTML.hyperlink(f'https://t.me/{username}', f'{full_name}')} ({HTML.mono(f'{user_id}')})\n"
    else:
        TEXT += f"{HTML.bold('User:')} {full_name} ({HTML.mono(f'{user_id}')})\n"
    keyboard = [
        [
            InlineKeyboardButton(text="Requsted Link", url=f"{link}"),
            InlineKeyboardButton(
                text="Pull Request",
                url=f"https://github.com/{PR_REPO}/pull/{pull.number}",
            ),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.effective_message.reply_html(
        text=TEXT,
        reply_markup=reply_markup,
        disable_web_page_preview=True,
    )


dump_handler = CommandHandler("dump", dump, filters=CustomFilters.authorized)
dispatcher.add_handler(dump_handler)
