from urllib.request import urlopen

from requests import head


# https://github.com/anasty17/mirror-leech-telegram-bot/blob/e0ae7026eb7d531924ad6a15fb2e2a2b33679612/bot/helper/ext_utils/bot_utils.py#L260
def get_content_type(link: str):
    try:
        res = head(
            link,
            allow_redirects=True,
            timeout=5,
            headers={"user-agent": "Wget/1.12"},
        )
        content_type = res.headers.get("content-type")
    except:
        try:
            res = urlopen(link, timeout=5)
            info = res.info()
            content_type = info.get_content_type()
        except:
            content_type = None
    return content_type


def check_link(link: str):
    required_formats = [
        "application/gzip",
        "application/vnd.rar",
        "application/x-7z-compressed",
        "application/zip",
        "application/x-tar",
        "application/x-gtar-compressed",
        "application/octet-stream",
        "application/java-archive",
        "application/x-gzip",
        "application/x-rar-compressed",
        "application/x-rar",
        "multipart/x-zip",
        "application/x-zip-compressed",
        "application/x-zip",
    ]
    content_format = get_content_type(link)
    if content_format in required_formats:
        return True
    else:
        return False
