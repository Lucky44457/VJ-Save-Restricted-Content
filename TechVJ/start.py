# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import asyncio
import pyrogram
import time
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserAlreadyParticipant, InviteHashExpired, UsernameNotOccupied
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from config import API_ID, API_HASH, ERROR_MESSAGE
from database.db import db
from TechVJ.strings import HELP_TXT

class batch_temp(object):
    IS_BATCH = {}

# =========================
# 🔁 Caption Replace Feature
# =========================

REPLACE_WORDS = {}

def apply_replace(user_id, caption):
    if not caption:
        return caption
    pair = REPLACE_WORDS.get(user_id)
    if pair:
        return caption.replace(pair[0], pair[1])
    return caption

@Client.on_message(filters.command("replace"))
async def set_replace(client, message):
    try:
        _, content = message.text.split(" ", 1)
        old, new = map(str.strip, content.split("|", 1))
        REPLACE_WORDS[message.from_user.id] = (old, new)
        await message.reply_text(f"✅ Will replace `{old}` with `{new}` in captions.", parse_mode="markdown")
    except:
        await message.reply_text("❌ Format wrong. Use:\n`/replace oldword | newword`", parse_mode="markdown")

@Client.on_message(filters.command("stopreplace"))
async def stop_replace(client, message):
    user_id = message.from_user.id
    if user_id in REPLACE_WORDS:
        REPLACE_WORDS.pop(user_id, None)
        await message.reply("🛑 Replace words cleared.")
    else:
        await message.reply("ℹ️ No replace settings were active.")

# (The rest of your code remains unchanged below...)

# ... All your downstatus, upstatus, progress, start, help, cancel and save commands remain as is ...

# Replace the line in handle_private:
# caption = msg.caption

# With:
caption = apply_replace(message.from_user.id, msg.caption)
