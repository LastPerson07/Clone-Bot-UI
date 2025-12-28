import os
from pyrogram import Client

if os.environ.get("ENV", False):
    from sample_config import Config, LOGGER
else:
    from config import Config, LOGGER

os.makedirs("sessions", exist_ok=True)

class User(Client):
    def __init__(self):
        super().__init__(
            "sessions/user",                   # 🔥 persistent
            api_id=Config.APP_ID,
            api_hash=Config.API_HASH,
            session_string=Config.TG_USER_SESSION,
            workers=4
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()

        me = await self.get_me()
        self.set_parse_mode("HTML")

        self.LOGGER(__name__).info(f"@{me.username} user account started!")

        return self, me.id

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("User stopped. Bye.")
