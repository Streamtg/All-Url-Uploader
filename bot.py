# MIT License

import os
import logging
import asyncio
import ntplib
from pyrogram import Client, idle
from config import Config

# -------------------- Configuración de logs --------------------
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# -------------------- Función de sincronización de hora --------------------
async def sync_time_google():
    """
    Sincroniza la hora del cliente con Google NTP.
    Retorna True si la sincronización fue exitosa.
    """
    try:
        client = ntplib.NTPClient()
        response = client.request('time.google.com')
        offset = response.offset
        if abs(offset) > 0.1:  # Ajuste solo si hay desfase significativo
            logger.info(f"[SYNC] Hora sincronizada con Google NTP, offset: {offset:.3f}s")
            await asyncio.sleep(offset)  # Ajuste interno del bot
        return True
    except Exception as e:
        logger.warning(f"[SYNC] No se pudo sincronizar la hora: {e}")
        return False

# -------------------- Función para iniciar el bot --------------------
async def start_bot():
    # Crear carpeta de descargas si no existe
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

    logger.info("Bot Starting...")

    # Sincronizamos la hora antes de iniciar Pyrogram
    await sync_time_google()

    await Uploadbot.start()
    logger.info("Bot Started :)")

    # Loop que sincroniza la hora antes de cada acción crítica (cada 30 min)
    async def periodic_sync():
        while True:
            await asyncio.sleep(1800)  # Cada 30 minutos
            await sync_time_google()

    # Ejecutamos el loop de sincronización en paralelo con idle()
    await asyncio.gather(
        periodic_sync(),
        idle()
    )

    await Uploadbot.stop()
    logger.info("Bot Stopped ;)")

# -------------------- Entrada principal --------------------
if __name__ == "__main__":
    asyncio.run(start_bot())
