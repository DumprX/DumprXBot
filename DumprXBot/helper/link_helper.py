from urllib.parse import urlparse
from urllib.request import urlopen

from cfscrape import create_scraper
from requests import head

from DumprXBot import CONTENT_FORMATS, LOGGER


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
    content_format = get_content_type(link)
    if content_format in CONTENT_FORMATS:
        return True
    else:
        return False


# https://github.com/anasty17/mirror-leech-telegram-bot/blob/bc0703f77ffe78b94e77e2958ffda5b542075dab/bot/helper/mirror_utils/download_utils/direct_link_generator.py
def get_direct_link(link: str):
    domain = urlparse(link).hostname
    if not domain:
        return "Invalid URL"
    if "we.tl" in domain or "wetransfer.com" in domain:
        return wetransfer(link)
    return "Bot only supports we.tl links for now."


def wetransfer(link: str):
    cget = create_scraper().request
    try:
        url = cget("GET", link).url
        json_data = {
            "security_hash": url.split("/")[-1],
            "intent": "entire_transfer",
        }
        res = cget(
            "POST",
            f'https://wetransfer.com/api/v4/transfers/{url.split("/")[-2]}/download',
            json=json_data,
        ).json()
        if "direct_link" in res:
            return res["direct_link"]
    except Exception as e:
        LOGGER.error(e.__class__.__name__)
