from NoobStuffs.libformatter import HTML

from DumprXBot import DEVS


def dev_check(func):
    def check_dev(update, context, *args, **kwargs):
        update.effective_chat.id
        user_id = update.effective_message.from_user.id or update.effective_user.id
        TEXT = f"{HTML.bold('You are not authorized to use this command!')}"
        if user_id not in DEVS:
            update.effective_message.reply_html(text=TEXT)
            return
        return func(update, context, *args, **kwargs)

    return check_dev
