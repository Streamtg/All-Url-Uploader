# MIT License

# Copyright (c) 2022 Hash Minner

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE

import os
import time
import logging
import ntplib
from pyrogram import Client, idle

# Configuración de logs
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from config import Config

# -------------------- Sincronización de hora --------------------
def sync_time():
    try:
        client = ntplib.NTPClient()
        response = client.request('pool.ntp.org')
        offset = response.offset
        if abs(offset) > 1:  # Solo ajusta si la diferencia es significativa
            logger.info(f"[INFO] Hora sincronizada con NTP, offset: {offset:.2f}s")
            time.sleep(offset)  # Ajuste del tiempo dentro de Python
        else:
            logger.info("[INFO] Hora local ya está sincronizada")
    except Exception as e:
        logger.warning(f"[WARN] No se pudo sincronizar la hora: {e}")

# ------------------------------------------------------------------

if __name__ == "__main__":
    # Sincronizamos la hora antes de iniciar el bot
    sync_time()

    # Creamos la carpeta de descargas si no existe
    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)

    plugins = dict(root="plugins")
    Uploadbot = Client(
        "All-Url-Uploader",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        plugins=plugins
    )

    logger.info("Bot Started :)")
    Uploadbot.run()
    idle()
    logger.info("Bot Stoped ;)")
