# MIT License
# Copyright (c) 2022 Hash Minner

from dotenv import load_dotenv
import os

load_dotenv()

class Config(object):

    # Get a token from @BotFather
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    BOT_USERNAME = os.environ.get("BOT_USERNAME")

    # Get these values from my.telegram.org
    API_ID = int(os.environ.get("API_ID", 0))
    API_HASH = os.environ.get("API_HASH")

    # TG Ids
    OWNER_ID = int(os.environ.get("OWNER_ID", 0))
    AUTH_USERS = [OWNER_ID] + [int(x) for x in os.environ.get("AUTH_USERS", "").split() if x]
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", 0))

    # No need to change
    ADL_BOT_RQ = {}
    DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_LOCATION", "./DOWNLOADS")
    CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", 128))
    TG_MAX_FILE_SIZE = int(os.environ.get("TG_MAX_FILE_SIZE", 4194304000))
    HTTP_PROXY = os.environ.get("HTTP_PROXY", "")
    PROCESS_MAX_TIMEOUT = int(os.environ.get("PROCESS_MAX_TIMEOUT", 3700))
