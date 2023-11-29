# CodeXBotz
# mrismanaziz

import os

from asyncio import sleep

from bot import Bot
from config import (
    BOT_TOKEN,
    CHANNEL_DB,
    ADMINS,
    LOGGER,
)
from pyrogram import filters
from pyrogram.types import Message


@Bot.on_message(filters.command("logs") & filters.user(ADMINS))
async def get_bot_logs(client: Bot, m: Message):
    bot_log_path = "logs.txt"
    if os.path.exists(bot_log_path):
        try:
            await m.reply_document(
                bot_log_path,
                quote=True,
            )
        except Exception as e:
            os.remove(bot_log_path)
            LOGGER(__name__).warning(e)
    elif not os.path.exists(bot_log_path):
        await m.reply_text("Tidak ada logs yang ditemukan!")


@Bot.on_message(filters.command("vars") & filters.user(ADMINS))
async def varsFunc(client: Bot, message: Message):
    msg = await message.reply_text("Tunggu Sebentar...")
    text = f"""<code>
BOT_TOKEN={BOT_TOKEN}
CHANNEL_DB={CHANNEL_DB}
ADMINS={ADMINS}
</code>"""
    await sleep(0.5)
    await msg.edit_text(text)
