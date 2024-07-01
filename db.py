from motor.motor_asyncio import AsyncIOMotorClient
import config

client = AsyncIOMotorClient(config.MONGO_URI)
db = client[config.MONGO_DB_NAME]
collection = db[config.MONGO_COLLECTION_NAME]