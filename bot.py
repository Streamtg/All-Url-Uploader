# MIT License

import os
import time
import logging
import asyncio
import ntplib
from pyrogram import Client, idle
from config import Config

# Configuración de logs
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# -------------------- Sincronización de hora con Google NTP --------------------
async def sync_time_google_loop(interval: int = 3600):
    """
    Sincroniza la hora con Google NTP periódicamente.
    interval: cada cuántos segundos se realiza la sincronización.
    """
    client = ntplib.NTPClient()
    while True:
        try:
            response = client.request('time.google.com')
            offset = response.offset
            if abs(offset) > 0.1:  # Solo ajustamos si el desfase > 0.1s
                logger.info(f"[SYNC] Hora sincronizada con Google NTP, offset: {offset:.3f}s")
                # Ajuste de tiempo interno del bot (solo para control, no cambia el sistema)
                await asyncio.sleep(offset)
            else:
                logger.info("[SYNC] Hora local ya está sincronizada")
        except Exception as e:
            logger.warning(f"[SYNC] No se pudo sincronizar la hora: {e}")
        await asyncio.sleep(interval)  # Espera hasta la siguiente sincronización

# ------------------------------------------------------------------

async def main():
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

    # Iniciamos el bot y el loop de sincronización en paralelo
    await asyncio.gather(
        Uploadbot.start(),
        sync_time_google_loop(interval=3600)  # Sincroniza cada hora
    )

    await idle()
    await Uploadbot.stop()
    logger.info("Bot Stopped ;)")

if __name__ == "__main__":
    asyncio.run(main())
