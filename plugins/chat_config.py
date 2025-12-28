# ----------------------------------- https://github.com/m4mallu/clonebot --------------------------------------------#
import asyncio
from bot import Bot
from presets import Presets
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from init import source_chat, destination_chat, source_message_id, dest_message_id, help_message_id


# ----------------------------- Start Message command function --------------------------- #
@Bot.on_message(filters.private & filters.command("start"))
async def start_bot(client: Bot, message: Message):
    usr = int(message.chat.id)

    try:
        help_message_id.pop(usr)
    except Exception:
        pass

    await message.reply_text(
        text=Presets.WELCOME_TEXT,
        parse_mode="HTML",   # 🔥 fixed
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("⏳ SOURCE", callback_data="source_btn"),
                 InlineKeyboardButton("🎯 DESTINATION", callback_data="dest_btn")],
                [InlineKeyboardButton("💡 VIEW CONFIG", callback_data="view_btn"),
                 InlineKeyboardButton("🚫 DEL CONFIG", callback_data="del_cfg_btn")],
                [InlineKeyboardButton("🌀 CLONE 🌀", callback_data="clone_btn")],
                [InlineKeyboardButton("❓ HELP", callback_data="help_btn"),
                 InlineKeyboardButton("❌ CLOSE", callback_data="close_btn")]
            ]
        )
    )


# -------------------------- Chat Id Input All-In-One function ---------------------------- #
@Bot.on_message(filters.private & filters.text & filters.reply)   # 🔥 fixed
async def chat_reply(client: Bot, message: Message):
    usr = int(message.from_user.id)
    user_bot_me = await client.USER.get_me()

    try:
        if message.reply_to_message.message_id == source_message_id[usr]:
            if str(message.text).startswith("-100") and message.text[1:].isdigit():
                bot_msg = await message.reply_text(Presets.WAIT_MSG)
                await asyncio.sleep(1)

                try:
                    if destination_chat.get(usr) == message.text:
                        await message.delete()
                        await client.delete_messages(message.chat.id, source_message_id[usr])
                        await bot_msg.edit(Presets.CHAT_DUPLICATED_MSG)
                        await asyncio.sleep(5)
                        await bot_msg.delete()
                        await start_bot(client, message)
                        return
                except:
                    pass

                try:
                    await client.USER.get_chat_member(int(message.text), int(user_bot_me.id))
                except:
                    await message.delete()
                    await bot_msg.edit(Presets.IN_CORRECT_PERMISSIONS_MESSAGE_SOURCE)
                    await client.delete_messages(message.chat.id, source_message_id[usr])
                    source_message_id.pop(usr, None)
                    await asyncio.sleep(5)
                    await bot_msg.delete()
                    await start_bot(client, message)
                    return

                source_chat[usr] = message.text
                await client.delete_messages(message.chat.id, source_message_id[usr])
                source_message_id.pop(usr, None)
                await message.delete()
                await bot_msg.edit(Presets.SOURCE_CONFIRM.format(message.text))
                await asyncio.sleep(2)
                await start_bot(client, message)
                return

    except:
        pass

    try:
        if message.reply_to_message.message_id == dest_message_id[usr]:
            if str(message.text).startswith("-100") and message.text[1:].isdigit():
                bot_msg = await message.reply_text(Presets.WAIT_MSG)
                await asyncio.sleep(1)

                try:
                    member = await client.USER.get_chat_member(int(message.text), int(user_bot_me.id))
                    if not member.can_post_messages:
                        raise Exception()
                except:
                    await client.delete_messages(message.chat.id, dest_message_id[usr])
                    await bot_msg.edit(Presets.IN_CORRECT_PERMISSIONS_MESSAGE_DEST_POSTING)
                    dest_message_id.pop(usr, None)
                    await asyncio.sleep(5)
                    await bot_msg.delete()
                    await start_bot(client, message)
                    return

                destination_chat[usr] = message.text
                await client.delete_messages(message.chat.id, dest_message_id[usr])
                dest_message_id.pop(usr, None)
                await message.delete()
                await bot_msg.edit(Presets.DESTINATION_CONFIRM.format(message.text))
                await asyncio.sleep(2)
                await start_bot(client, message)
                return
    except:
        pass


# ----------------------------- Help Function --------------------------- #
async def help_me(client: Bot, message: Message):
    usr = int(message.chat.id)

    msg_help = await message.reply_text(
        text=Presets.HELP_TEXT.format(message.from_user.first_name),
        parse_mode="HTML",   # 🔥 fixed
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🏠 HOME", callback_data="home_btn")]]
        )
    )

    help_message_id[usr] = msg_help.message_id

    await asyncio.sleep(30)

    if help_message_id.get(usr) == msg_help.message_id:
        await msg_help.delete()
        await start_bot(client, message)
