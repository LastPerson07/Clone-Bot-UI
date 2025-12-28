import os
import logging
from logging.handlers import RotatingFileHandler

# Logging setup (taken from original clonebot)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            "clonebot-ui.txt",
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)

logging.getLogger("pyrogram").setLevel(logging.WARNING)

class Config(object):
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
    APP_ID       = int(os.environ.get("APP_ID", "0"))
    API_HASH     = os.environ.get("API_HASH", "")
    TG_USER_SESSION = os.environ.get("TG_USER_SESSION", "")

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
