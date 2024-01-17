import asyncio

from hydrogram import Client, filters
from hydrogram.errors import FloodWait
from hydrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from core import Bot
from core.config import ADMINS, CHANNEL_DB, DISABLE_BUTTON, LOGGER
from core.func import encode


@Bot.on_message(
    filters.private
    & filters.user(ADMINS)
    & ~filters.command(
        [
            "start",
            "help",
            "ping",
            "uptime",
            "log",
            "users",
            "batch",
            "broadcast"
        ]
    )
)
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Sedang diproses...", quote=True)
    try:
        post_message = await message.copy(
            chat_id=client.db_channel.id, disable_notification=True
        )
    except FloodWait as e:
        await asyncio.sleep(e.value)
        post_message = await message.copy(
            chat_id=client.db_channel.id, disable_notification=True
        )
    except Exception as e:
        LOGGER(__name__).warning(e)
        await reply_text.edit_text("Error!")
        return
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"

    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Bagikan Link", url=f"https://telegram.me/share/url?url={link}"
                )
            ]
        ]
    )

    await reply_text.edit(
        f"Link: {link}",
        reply_markup=reply_markup,
        disable_web_page_preview=True,
    )

    if not DISABLE_BUTTON:
        try:
            await post_message.edit_reply_markup(reply_markup)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await post_message.edit_reply_markup(reply_markup)
        except Exception:
            pass


@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_DB))
async def new_post(client: Client, message: Message):
    if DISABLE_BUTTON:
        return
    
    converted_id = message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Bagikan Link", url=f"https://telegram.me/share/url?url={link}"
                )
            ]
        ]
    )
    try:
        await message.edit_reply_markup(reply_markup)
    except FloodWait as e:
        await asyncio.sleep(e.value)
        await message.edit_reply_markup(reply_markup)
    except Exception:
        pass
