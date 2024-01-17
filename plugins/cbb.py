# CodeXBotz 
# mrismanaziz

from bot import Bot
from Data import Data

from hydrogram import filters
from hydrogram.errors import MessageNotModified
from hydrogram.types import CallbackQuery, InlineKeyboardMarkup, Message


@Bot.on_message(filters.private & filters.incoming & filters.command("about"))
async def _about(client: Bot, msg: Message):
    await client.send_message(
        msg.chat.id,
        Data.ABOUT.format(client.username),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(Data.mbuttons),
    )


@Bot.on_message(filters.private & filters.incoming & filters.command("help"))
async def _help(client: Bot, msg: Message):
    await client.send_message(
        msg.chat.id, 
        Data.HELP,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(Data.buttons),
    )


@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        try:
            await query.message.edit_text(
                text=Data.ABOUT.format(client.username),
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(Data.mbuttons),
            )
        except MessageNotModified:
            pass
    elif data == "help":
        try:
            await query.message.edit_text(
                text=Data.HELP,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(Data.buttons),
            )
        except MessageNotModified:
            pass
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except Exception:
            pass
