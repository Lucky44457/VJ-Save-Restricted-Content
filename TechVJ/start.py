import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from config import API_ID, API_HASH  # tumhare config.py me ye already hai

# Session folder banaye
if not os.path.exists("sessions"):
    os.makedirs("sessions")

# User session path
def get_session_path(phone):
    return os.path.join("sessions", f"{phone}.session")

async def login(phone):
    session_path = get_session_path(phone)
    if os.path.exists(session_path):
        print(f"[+] Existing session mila: {session_path}")
        client = TelegramClient(session_path, API_ID, API_HASH)
        await client.connect()
        if not await client.is_user_authorized():
            print("[-] Session expired. Please login again.")
            await client.start(phone)
        return client
    else:
        print("[*] Pehli baar login ho raha hai...")
        client = TelegramClient(session_path, API_ID, API_HASH)
        await client.start(phone)
        print(f"[+] Session save ho gaya: {session_path}")
        return client

async def forward_messages(client, source_chat, target_chat, start_id, end_id):
    for msg_id in range(start_id, end_id + 1):
        try:
            msg = await client.get_messages(source_chat, ids=msg_id)
            if msg:
                await client.send_message(target_chat, msg)
                print(f"[+] Forwarded {msg_id}")
            await asyncio.sleep(1)  # rate limit
        except Exception as e:
            print(f"[-] Error {msg_id}: {e}")

async def main():
    phone_number = input("Enter your phone number (with country code): ")
    client = await login(phone_number)

    # Example forward
    source = input("Source chat username/link/id: ")
    target = input("Target chat username/link/id: ")
    start_id = int(input("Start message ID: "))
    end_id = int(input("End message ID: "))

    await forward_messages(client, source, target, start_id, end_id)
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
