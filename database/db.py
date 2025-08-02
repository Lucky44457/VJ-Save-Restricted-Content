import motor.motor_asyncio
from config import DB_NAME, DB_URI

class Database:
    
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users

    def new_user(self, id, name):
        return dict(
            id=id,
            name=name,
            session=None,
            replace={"old": None, "new": None},  # Added replace field
        )
    
    async def add_user(self, id, name):
        user = self.new_user(id, name)
        await self.col.insert_one(user)
    
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return bool(user)
    
    async def total_users_count(self):
        return await self.col.count_documents({})

    async def get_all_users(self):
        return self.col.find({})

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

    async def set_session(self, id, session):
        await self.col.update_one({'id': int(id)}, {'$set': {'session': session}})

    async def get_session(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('session')

    # ✅ NEW: Set replace rule
    async def set_replace(self, id, old, new):
        await self.col.update_one(
            {'id': int(id)},
            {'$set': {'replace': {'old': old, 'new': new}}}
        )

    # ✅ NEW: Get replace rule
    async def get_replace(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('replace', {"old": None, "new": None})

    # ✅ NEW: Clear replace rule
    async def clear_replace(self, id):
        await self.col.update_one(
            {'id': int(id)},
            {'$set': {'replace': {'old': None, 'new': None}}}
        )

db = Database(DB_URI, DB_NAME)
