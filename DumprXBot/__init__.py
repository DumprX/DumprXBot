import logging
import os
import time

from dotenv import load_dotenv
from telegram.ext import Updater

StartTime = time.time()

logging.basicConfig(
    format="[%(asctime)s - %(name)s] %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[logging.FileHandler(f"{__name__}.log"), logging.StreamHandler()],
    level=logging.INFO,
)
LOGGER = logging.getLogger(__name__)

load_dotenv("config.env")


def getConfig(config_name):
    return os.environ[config_name]


try:
    BOT_TOKEN = getConfig("BOT_TOKEN")
    CHAT_ID = int(getConfig("CHAT_ID"))
    GH_TOKEN = getConfig("GH_TOKEN")
    GH_USER = getConfig("GH_USER")
    GH_EMAIL = getConfig("GH_EMAIL")
    PR_REPO = getConfig("PR_REPO")
    PR_REPO_BRANCH = getConfig("PR_REPO_BRANCH")
    DEVS = [int(DEV) for DEV in getConfig("DEVS").split(" ")]
except Exception as error:
    LOGGER.error("Fill all configs plox\nExiting...")
    exit(0)

UNAUTHORIZED_CHATS_ENCOUTER = []

updater = Updater(token=BOT_TOKEN)
dispatcher = updater.dispatcher
