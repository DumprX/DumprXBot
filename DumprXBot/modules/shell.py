import subprocess

from NoobStuffs.libformatter import HTML
from telegram import ParseMode, Update
from telegram.constants import MAX_MESSAGE_LENGTH
from telegram.ext import CallbackContext, CommandHandler

from DumprXBot import dispatcher
from DumprXBot.helper import CustomFilters, dev_check


@dev_check
def shell(update: Update, context: CallbackContext):
    command = update.message.text.split(" ", 1)
    if len(command) == 1:
        return update.effective_message.reply_html(
            text="Plox give any command to execute.",
        )
    command = command[1]
    message = update.effective_message.reply_html(
        text=f"{HTML.bold('Executing:')} {HTML.mono(f'{command}...')}",
    )
    process = subprocess.Popen(
        args=command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    return_code = process.wait()
    stdout, stderr = process.communicate()
    if stdout:
        output = stdout.decode()
    if stderr:
        output = stderr.decode()
    TEXT = f"{HTML.bold('Command:')} {HTML.mono(f'{command}')}\n"
    TEXT += f"{HTML.bold('Return Code:')} {HTML.mono(f'{return_code}')}\n\n"
    if len(output) + len(TEXT) < MAX_MESSAGE_LENGTH:
        TEXT += f"{HTML.bold('Output:')}\n"
        TEXT += f"{HTML.mono(f'{output}')}"
        message.edit_text(text=TEXT, parse_mode=ParseMode.HTML)
    else:
        with open("output.txt", "w") as out:
            out.write(output)
        TEXt += f"{HTML.bold('Output:')} {HTML.mono('Sent as document')}"
        message.delete()
        with open("output.txt", "rb") as out:
            update.effective_message.reply_document(
                document=out,
                filename="output.txt",
                caption=TEXT,
                parse_mode=ParseMode.HTML,
            )


shell_handler = CommandHandler("shell", shell, filters=CustomFilters.authorized)
dispatcher.add_handler(shell_handler)
