# MIT License
# Copyright ...

import os
import asyncio
import logging
from pyrogram import Client, idle
from pyrogram.errors import SessionRevoked, RPCError, Unauthorized, FloodWait

from config import Config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

async def start_bot():
    """Función principal para iniciar el bot."""
    try:
        logger.info("Bot Starting...")

        # Asegurar directorio de descargas
        if not os.path.isdir(Config.DOWNLOAD_LOCATION):
            os.makedirs(Config.DOWNLOAD_LOCATION)

        plugins = dict(root="plugins")

        Uploadbot = Client(
            "All-Url-Uploader",
            bot_token=Config.BOT_TOKEN,
            api_id=int(Config.API_ID),
            api_hash=Config.API_HASH,
            plugins=plugins
        )

        try:
            await Uploadbot.start()
            logger.info("Bot Started ✅")
            await idle()
        except SessionRevoked:
            logger.error("❌ Sesión revocada por Telegram. Revisa tu BOT_TOKEN.")
        except Unauthorized:
            logger.error("❌ Credenciales inválidas. Revisa API_ID, API_HASH o BOT_TOKEN.")
        except FloodWait as e:
            logger.warning(f"⏳ FloodWait: espera {e.value} segundos.")
            await asyncio.sleep(e.value)
        except RPCError as e:
            logger.error(f"⚠️ RPCError: {e}")
        except Exception as e:
            logger.error(f"⚠️ Error inesperado: {e}")
        finally:
            if Uploadbot.is_connected:
                await Uploadbot.stop()
            logger.info("Bot Stopped 🛑")

    except Exception as e:
        logger.critical(f"💥 Error crítico al iniciar: {e}")


if __name__ == "__main__":
    asyncio.run(start_bot())
