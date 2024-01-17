from os import getenv
from dotenv import load_dotenv
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


BOT_TOKEN = getenv("BOT_TOKEN")

CHANNEL_DB = int(getenv("CHANNEL_DB"))
DATABASE_URL = getenv("DATABASE_URL")
DATABASE_NAME = getenv("DATABASE_NAME")

RESTRICT = getenv("RESTRICT", True)

FORCE_SUB_ = {}
FSUB_TOTAL = 1
while True:
    key = f"FORCE_SUB_{FSUB_TOTAL}"
    value = getenv(key)
    if value is None:
        break
    FORCE_SUB_[FSUB_TOTAL] = int(value)
    FSUB_TOTAL += 1

BUTTON_ROW = int(getenv("BUTTON_ROW", 3))
BUTTON_TITLE = getenv("BUTTON_TITLE", "Join")


START_MESSAGE = getenv(
    "START_MESSAGE",
    "Halo {mention}!"
    "\n\n"
    "Saya dapat menyimpan file pribadi di Channel tertentu dan pengguna lain dapat mengaksesnya dari link khusus.",
)
FORCE_MESSAGE = getenv(
    "FORCE_MESSAGE",
    "Halo {mention}!"
    "\n\n"
    "Anda harus bergabung di Channel/Group terlebih dahulu untuk melihat file yang saya bagikan."
    "\n\n"
    "Silakan Join Ke Channel/Group terlebih dahulu.",
)

try:
    ADMINS = [int(x) for x in (getenv("ADMINS").split())]
except ValueError:
    raise Exception("Daftar Admin Anda tidak berisi User ID Telegram yang valid.")
    
CUSTOM_CAPTION = getenv("CUSTOM_CAPTION", None)
DISABLE_BUTTON = getenv("DISABLE_BUTTON", False)


LOGS_FILE = "log.txt"
basicConfig(
    level=INFO,
    format="[%(levelname)s] - %(message)s",
    handlers=[
        RotatingFileHandler(LOGS_FILE, maxBytes=50000000, backupCount=10),
        StreamHandler(),
    ],
)
getLogger("hydrogram").setLevel(WARNING)
def LOGGER(name: str) -> Logger:
    return getLogger(name)