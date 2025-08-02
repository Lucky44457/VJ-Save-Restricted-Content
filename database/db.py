from motor.motor_asyncio import AsyncIOMotorClient
from config import DB_URI, DB_NAME

class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(DB_URI)
        self.db = self.client[DB_NAME]
        self.users = self.db.users

    async def is_user_exist(self, user_id):
        return await self.users.find_one({"user_id": user_id}) is not None

    async def add_user(self, user_id, name):
        await self.users.insert_one({
            "user_id": user_id,
            "name": name,
            "replace": None
        })

    async def set_replace(self, user_id, old, new):
        await self.users.update_one(
            {"user_id": user_id},
            {"$set": {"replace": {"old": old, "new": new}}}
        )

    async def get_replace(self, user_id):
        user = await self.users.find_one({"user_id": user_id})
        return user.get("replace") if user else None

    async def clear_replace(self, user_id):
        await self.users.update_one(
            {"user_id": user_id},
            {"$set": {"replace": None}}
        )

db = Database()
