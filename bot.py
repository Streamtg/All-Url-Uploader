# MIT License
# Copyright (c) 2022 Hash Minner
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE

import os
import asyncio
import logging
from pyrogram import Client, idle
from config import Config

# ----------------- Logging -----------------
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# ----------------- OpenCC Pure Python -----------------
try:
    from opencc_reimplemented import OpenCC
    cc = OpenCC('s2t')  # Example: Simplified -> Traditional
except ImportError:
    cc = None
    logger.warning("OpenCC Python pure implementation not installed. Text conversion disabled.")

# ----------------- Bot -----------------
async def start_bot():
    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)

    plugins = dict(root="plugins")
    Uploadbot = Client("All-Url-Uploader",
                       bot_token=Config.BOT_TOKEN,
                       api_id=Config.API_ID,
                       api_hash=Config.API_HASH,
                       plugins=plugins)
    try:
        logger.info("Bot Starting...")
        await Uploadbot.start()
        logger.info("Bot Started :)")
        await idle()
    finally:
        await Uploadbot.stop()
        logger.info("Bot Stopped ;)")

if __name__ == "__main__":
    # Ejecuta el bot
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        logger.info("Bot manually stopped.")
