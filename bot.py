import os
from pyrogram import Client
from user import User

# Load config
if bool(os.environ.get("ENV", False)):
    from sample_config import Config, LOGGER
else:
    from config import Config, LOGGER


class Bot(Client):
    USER: User = None
    USER_ID: int = None

    def __init__(self):
        super().__init__(
            "bot_session",
            api_id=Config.APP_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.TG_BOT_TOKEN,
            sleep_threshold=30,
            plugins={"root": "plugins"},
            no_updates=True      # this is enough
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.set_parse_mode("HTML")
        self.LOGGER(__name__).info(f"@{me.username} started!")
        self.USER, self.USER_ID = await User().start()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped. Bye.")


if __name__ == "__main__":
    os.makedirs("sessions", exist_ok=True)
    bot = Bot()
    bot.run()   # 🔥 correct for Pyrogram 2.0.106
