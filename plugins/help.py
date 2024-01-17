from core import Bot

from hydrogram import filters
from hydrogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from hydrogram.types import InlineKeyboardButton


class Data:
    HELP = """
Pengguna Bot
  /start - Mulai
  /about - Tentang
  /help - Bantuan
  /ping - Latensi bot
  /uptime - Waktu aktif
 
Admin Bot
  /log - Mengambil log
  /users - Statistik pengguna
  /batch - Multi post dalam satu link)
  /broadcast - Pesan siaran
"""

    close = [
        [InlineKeyboardButton("Tutup", callback_data="close")]
    ]

    mbuttons = [
        [
            InlineKeyboardButton("Bantuan", callback_data="help"),
            InlineKeyboardButton("Tutup", callback_data="close")
        ],
    ]

    buttons = [
        [
            InlineKeyboardButton("Tentang", callback_data="about"),
            InlineKeyboardButton("Tutup", callback_data="close")
        ],
    ]

    ABOUT = """
@{} adalah Bot untuk menyimpan postingan atau file yang dapat diakses melalui link khusus.

  Framework: <a href='https://docs.hydrogram.org'>hydrogram</a>
  Re-Code From: <a href='https://github.com/mrismanaziz/File-Sharing-Man'>File-Sharing-Man</a>
"""


@Bot.on_message(filters.private & filters.incoming & filters.command("help"))
async def help(client: Bot, message: Message):
    await client.send_message(
        message.chat.id, 
        Data.HELP,
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(Data.buttons),
    )


@Bot.on_callback_query()
async def handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        try:
            await query.message.edit_text(
                text=Data.ABOUT.format(client.username),
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(Data.mbuttons),
            )
        except Exception:
            pass
    elif data == "help":
        try:
            await query.message.edit_text(
                text=Data.HELP,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(Data.buttons),
            )
        except Exception:
            pass
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except Exception:
            pass