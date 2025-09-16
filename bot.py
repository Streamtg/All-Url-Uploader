# MIT License
# Copyright (c) 2022 Hash Minner
# [Licencia resumida para no repetir]

import os
import asyncio
import logging
from pyrogram import Client, idle
from pyrogram.errors import SessionRevoked, RPCError, ConnectionError
from config import Config

# Configuración de logs
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

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

    # Intentar iniciar sesión con manejo de errores
    try:
        logger.info("Bot Starting...")
        await Uploadbot.start()
        logger.info("Bot Started :)")
        await idle()
    except SessionRevoked:
        logger.warning("La sesión fue revocada. Eliminando archivo de sesión y reiniciando...")
        # Elimina cualquier sesión vieja
        session_file = "All-Url-Uploader.session"
        if os.path.exists(session_file):
            os.remove(session_file)
        # Reinicia el bot
        await Uploadbot.stop()
        await start_bot()
    except RPCError as e:
        logger.error(f"Error RPC: {e}")
    except ConnectionError:
        logger.warning("Cliente ya estaba terminado, ignorando...")
    finally:
        # Asegurarse de detener el cliente correctamente
        if Uploadbot.is_connected:
            await Uploadbot.stop()
        logger.info("Bot Stopped ;)")

if __name__ == "__main__":
    asyncio.run(start_bot())
