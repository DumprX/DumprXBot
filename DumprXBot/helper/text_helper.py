from html import escape


def bold(text):
    return f"<b>{escape(text)}</b>"


def mono(text):
    return f"<code>{escape(text)}</code>"


def hyperlink(link, text):
    return f"<a href='{link}'>{escape(text)}</a>"
