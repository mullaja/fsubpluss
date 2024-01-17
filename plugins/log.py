from os import remove
from os.path import exists

from core import Bot
from core.config import ADMINS, LOGGER
from hydrogram import filters
from hydrogram.types import Message


@Bot.on_message(filters.command("log") & filters.user(ADMINS))
async def logs(client: Bot, message: Message):
    logs_path = "log.txt"
    if exists(logs_path):
        try:
            await message.reply_document(
                logs_path,
                quote=True,
            )
        except Exception as e:
            remove(logs_path)
            LOGGER(__name__).warning(e)
    elif not path.exists(logs_path):
        await message.reply_text("Tidak ada logs yang ditemukan!")
