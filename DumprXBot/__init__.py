import logging
import os
import time

from dotenv import load_dotenv
from NoobStuffs.liblogging import setup_logging
from telegram.ext import Updater

StartTime = time.time()

LOGGER = setup_logging("DumprXBot")

load_dotenv("config.env")


def getConfig(config_name):
    return os.environ[config_name]


CONTENT_FORMATS = []
UNAUTHORIZED_CHATS_ENCOUTER = []

try:
    BOT_TOKEN = getConfig("BOT_TOKEN")
    CHAT_IDS = {int(CHAT_ID) for CHAT_ID in getConfig("CHAT_IDS").split(" ")}
    GH_TOKEN = getConfig("GH_TOKEN")
    GH_USER = getConfig("GH_USER")
    GH_EMAIL = getConfig("GH_EMAIL")
    PR_REPO = getConfig("PR_REPO")
    PR_REPO_BRANCH = getConfig("PR_REPO_BRANCH")
    DEVS = {int(DEV) for DEV in getConfig("DEVS").split(" ")}
except Exception as error:
    LOGGER.error("Fill all configs plox\nExiting...")
    exit(0)

try:
    CONTENTS = {str(x) for x in getConfig("CONTENT_FORMATS").split(" ")}
except:
    CONTENTS = None

try:
    DB_URL = getConfig("DB_URL")
except:
    DB_URL = None

if CONTENTS is not None:
    for cformat in CONTENTS:
        CONTENT_FORMATS.append(cformat)

updater = Updater(token=BOT_TOKEN)
dispatcher = updater.dispatcher
