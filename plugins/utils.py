# CodeXBotz
# mrismanaziz


from os import remove
from os.path import exists

from asyncio import sleep

from bot import Bot
from config import ADMINS, LOGGER
from pyrogram import filters
from pyrogram.types import Message


@Bot.on_message(filters.command("logs") & filters.user(ADMINS))
async def logs(client: Bot, message: Message):
    logs_path = "logs.txt"
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
