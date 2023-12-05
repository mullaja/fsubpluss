# Codexbotz 
# @mrismanaziz


from os import environ
from dotenv import load_dotenv
from distutils.util import strtobool
from logging.handlers import RotatingFileHandler
from logging import(
    basicConfig, 
    INFO, 
    WARNING, 
    StreamHandler, 
    getLogger,
    Logger
)

load_dotenv("config.env")


BOT_TOKEN = environ.get("BOT_TOKEN", "")

CHANNEL_DB = int(environ.get("CHANNEL_DB", ""))
DATABASE_URL = environ.get("DATABASE_URL", "")
DATABASE_NAME = environ.get("DATABASE_NAME", "")

RESTRICT = strtobool(environ.get("RESTRICT", "True"))

FORCE_SUB_ = {}
FSUB_TOTAL = 1
while True:
    key = f"FORCE_SUB_{FSUB_TOTAL}"
    value = environ.get(key)
    if value is None:
        break
    FORCE_SUB_[FSUB_TOTAL] = int(value)
    FSUB_TOTAL += 1

BUTTON_ROW = int(environ.get("BUTTON_ROW", "3"))
BUTTON_TITLE = environ.get("BUTTON_TITLE", "Join")


START_MESSAGE = environ.get(
    "START_MESSAGE",
    "Halo {mention}!"
    "\n\n"
    "Saya dapat menyimpan file pribadi di Channel tertentu dan pengguna lain dapat mengaksesnya dari link khusus.",
)
FORCE_MESSAGE = environ.get(
    "FORCE_MESSAGE",
    "Halo {mention}!"
    "\n\n"
    "Anda harus bergabung di Channel/Group terlebih dahulu untuk melihat file yang saya bagikan."
    "\n\n"
    "Silakan Join Ke Channel/Group terlebih dahulu.",
)

try:
    ADMINS = [int(x) for x in (environ.get("ADMINS", "").split())]
except ValueError:
    raise Exception("Daftar Admin Anda tidak berisi User ID Telegram yang valid.")
    
CUSTOM_CAPTION = environ.get("CUSTOM_CAPTION", None)
DISABLE_BUTTON = strtobool(environ.get("DISABLE_BUTTON", "False"))


LOGS_FILE = "logs.txt"
basicConfig(
    level=INFO,
    format="[%(levelname)s] - %(message)s",
    handlers=[
        RotatingFileHandler(LOGS_FILE, maxBytes=50000000, backupCount=10),
        StreamHandler(),
    ],
)
getLogger("pyrogram").setLevel(WARNING)
def LOGGER(name: str) -> Logger:
    return getLogger(name)