import os
from telethon import TelegramClient
from config import API_ID, API_HASH, PHONE_NUMBER

# Sessions folder create
SESSIONS_DIR = os.path.join(os.path.dirname(__file__), "sessions")
os.makedirs(SESSIONS_DIR, exist_ok=True)

# Session file ka naam phone number ke saath
session_path = os.path.join(SESSIONS_DIR, f"{PHONE_NUMBER}.session")

# Telethon client
client = TelegramClient(session_path, API_ID, API_HASH)

async def main():
    # Agar pehli baar login hai
    if not os.path.exists(session_path):
        print("📲 First time login — sending code...")
        await client.start(phone=PHONE_NUMBER)
        print(f"✅ Session saved: {session_path}")
    else:
        # Dusri baar se direct login
        await client.connect()
        if not await client.is_user_authorized():
            print("⚠ Session expired, please login again.")
            await client.start(phone=PHONE_NUMBER)
            print(f"✅ Session re-saved: {session_path}")

    me = await client.get_me()
    print(f"✅ Logged in as {me.first_name} ({me.id})")

with client:
    client.loop.run_until_complete(main())
