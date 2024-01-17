# CodeXBotz 
# mrismanaziz

import asyncio

from datetime import datetime
from time import time

from bot import Bot
from config import (
    ADMINS,
    CUSTOM_CAPTION,
    DISABLE_BUTTON,
    FORCE_MESSAGE,
    RESTRICT,
    START_MESSAGE,
)
from database.mongo import add_user, del_user, full_userbase, present_user

from hydrogram import filters
from hydrogram.errors import FloodWait
from hydrogram.types import InlineKeyboardMarkup, Message

from helper_func import(
    decode,
    get_messages, 
    subs,
)

from .button import fsub_button, start_button

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60**2 * 24),
    ("hour", 60**2),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append(f'{amount} {unit}{"" if amount == 1 else "s"}')
    return ", ".join(parts)


@Bot.on_message(filters.command("start") & filters.private & subs )
async def start_command(client: Bot, message: Message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except Exception:
            pass
    text = message.text
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
        except Exception:
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except Exception:
                return
            if start <= end:
                ids = range(start, end + 1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except Exception:
                return
        temp_msg = await message.reply("Sedang diproses...")
        try:
            messages = await get_messages(client, ids)
        except Exception:
            await message.reply_text("Error!")
            return
        await temp_msg.delete()

        for msg in messages:
            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(
                    previouscaption=msg.caption.html if msg.caption else "",
                    filename=msg.document.file_name,
                )

            else:
                caption = msg.caption.html if msg.caption else ""
                reply_markup = msg.reply_markup if DISABLE_BUTTON else None
            try:
                await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    protect_content=RESTRICT,
                    reply_markup=reply_markup,
                )
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    protect_content=RESTRICT,
                    reply_markup=reply_markup,
                )
            except Exception:
                pass
    else:
        buttons = start_button(client)
        await message.reply_text(
            text=START_MESSAGE.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None 
                if not message.from_user.username
                else "@" + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id,
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True,
            quote=True,
        )

    return


@Bot.on_message(filters.command("start") & filters.private)
async def not_joined(client: Bot, message: Message):
    buttons = fsub_button(client, message)
    await message.reply(
        text=FORCE_MESSAGE.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=f"@{message.from_user.username}"
            if message.from_user.username
            else None,
            mention=message.from_user.mention,
            id=message.from_user.id,
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
        disable_web_page_preview=True,
    )


@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(message.chat.id, "Mengecek...")
    users = await full_userbase()
    await msg.edit(f"{len(users)} Pengguna Bot")



@Bot.on_message(filters.command("broadcast") & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        unsuccessful = 0

        please_wait = await message.reply(
            "Mengirim pesan siaran..."
        )
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id, protect_content=RESTRICT)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.value)
                await broadcast_msg.copy(chat_id, protect_content=RESTRICT)
                successful += 1
            except Exception:
                await del_user(chat_id)
                unsuccessful += 1
                pass
            total += 1
        status = f"""
Status Broadcast
Pengguna: {total}
Berhasil: {successful}
Gagal: {unsuccessful}
* Termasuk Bot Admins
"""
        return await please_wait.edit(status)
    else:
        msg = await message.reply(
            "Balas ke pesan!"
        )
        await msg.delete()


@Bot.on_message(filters.command("ping"))
async def ping_pong(client, m: Message):
    start = time()
    m_reply = await m.reply_text("...")
    delta_ping = time() - start
    await m_reply.edit_text(
        f"Hasil: {delta_ping * 1000:.3f}ms"
    )


@Bot.on_message(filters.command("uptime"))
async def get_uptime(client, m: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await m.reply_text(
        f"Waktu Aktif: {uptime}\n"
        f"Sejak: {START_TIME_ISO}"
    )
