import os
import asyncio
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
from config import API_ID, API_HASH, SOURCE_CHAT, DESTINATION

# Make sure sessions folder exists
if not os.path.exists("sessions"):
    os.makedirs("sessions")

async def main():
    phone = input("📱 Enter your phone number (with country code): ").strip()
    session_path = f"sessions/{phone}.session"

    # If session exists, use it directly
    if os.path.exists(session_path):
        print(f"✅ Using existing session for {phone}")
        client = TelegramClient(session_path, API_ID, API_HASH)
        await client.start()
    else:
        # First-time login
        client = TelegramClient(session_path, API_ID, API_HASH)
        await client.connect()

        if not await client.is_user_authorized():
            try:
                await client.send_code_request(phone)
                code = input("🔑 Enter the code you received: ").strip()
                await client.sign_in(phone, code)
            except SessionPasswordNeededError:
                pw = input("🔒 Enter your 2FA password: ").strip()
                await client.sign_in(password=pw)

        print(f"✅ Logged in and session saved as {session_path}")

    # Event handler: forward from SOURCE_CHAT to DESTINATION
    @client.on(events.NewMessage(chats=SOURCE_CHAT))
    async def handler(event):
        try:
            await client.forward_messages(DESTINATION, event.message)
            print(f"📨 Forwarded message ID {event.message.id}")
        except Exception as e:
            print(f"⚠️ Error forwarding message: {e}")

    print("🚀 Bot is running...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
