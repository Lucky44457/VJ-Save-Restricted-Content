import os
from telethon import TelegramClient, events
from config import API_ID, API_HASH, BOT_TOKEN

# Make sure sessions folder exists
SESSIONS_DIR = os.path.join(os.path.dirname(__file__), "sessions")
os.makedirs(SESSIONS_DIR, exist_ok=True)

# Function to get or create a user session
def get_client(phone_number: str):
    session_path = os.path.join(SESSIONS_DIR, f"{phone_number}.session")
    return TelegramClient(session_path, API_ID, API_HASH)

# -------- Bot for user login --------
async def start_user_login():
    phone = input("Enter your phone number (with country code, e.g. +91xxxx): ").strip()
    client = get_client(phone)
    await client.start(phone)
    print(f"✅ Logged in successfully. Session saved at: sessions/{phone}.session")
    await client.run_until_disconnected()

# -------- Bot that forwards from private channels --------
bot = TelegramClient("bot_session", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage(pattern="/start"))
async def start_command(event):
    await event.respond("Welcome! This bot forwards messages from a private channel. Your session is already saved.")

@bot.on(events.NewMessage(pattern="/forward"))
async def forward_command(event):
    # Example forward logic — replace with your own
    source_chat = -100123456789  # source private channel ID
    target_chat = event.chat_id  # where to forward
    async for message in bot.iter_messages(source_chat, limit=10):
        await bot.send_message(target_chat, message)

if __name__ == "__main__":
    mode = input("Enter mode (login/bot): ").strip().lower()
    if mode == "login":
        import asyncio
        asyncio.run(start_user_login())
    elif mode == "bot":
        print("🤖 Bot is running...")
        bot.run_until_disconnected()
    else:
        print("❌ Invalid mode. Use 'login' or 'bot'.")
