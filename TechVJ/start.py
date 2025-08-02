from pyrogram import Client, filters
from pyrogram.types import Message
from Database.db import db  # Correct import for db.py in Database/ folder

# /start command
@Client.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
    await message.reply_text(
        "👋 Welcome! Send any media and I'll save it.\n\n"
        "Set caption replace using:\n/replace old | new\n\n"
        "Clear it:\n/clearreplace"
    )

# /replace command
@Client.on_message(filters.command("replace") & filters.private)
async def replace_command(client, message: Message):
    try:
        _, data = message.text.split(" ", 1)
        old, new = [s.strip() for s in data.split("|", 1)]
    except Exception:
        return await message.reply_text("❌ Usage:\n/replace old | new")

    await db.set_replace(message.from_user.id, old, new)
    await message.reply_text(f"✅ Rule saved:\n`{old}` ➝ `{new}`", parse_mode="markdown")

# /clearreplace command
@Client.on_message(filters.command("clearreplace") & filters.private)
async def clear_replace_command(client, message: Message):
    await db.clear_replace(message.from_user.id)
    await message.reply_text("✅ Replace rule cleared.")

# Handle media
@Client.on_message(filters.private & (filters.video | filters.document | filters.photo | filters.audio))
async def handle_private(client, message: Message):
    if not message.from_user:
        return

    replace = await db.get_replace(message.from_user.id)
    caption = message.caption or ""

    if isinstance(replace, dict):
        old_text = replace.get("old")
        new_text = replace.get("new")
        if old_text and new_text and isinstance(caption, str):
            caption = caption.replace(old_text, new_text)

    if message.video:
        await message.reply_video(video=message.video.file_id, caption=caption)
    elif message.document:
        await message.reply_document(document=message.document.file_id, caption=caption)
    elif message.photo:
        await message.reply_photo(photo=message.photo.file_id, caption=caption)
    elif message.audio:
        await message.reply_audio(audio=message.audio.file_id, caption=caption)
