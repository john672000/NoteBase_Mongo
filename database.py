from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
print(f'Environment set URI = {MONGO_URI}')
MONGO_DB = "test"

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    # Try pinging the server
    client.admin.command("ping")
    print(f"✅ Connected to MongoDB at {MONGO_URI}")
    print(f"📂 Using database: {MONGO_DB}")
    print(f"🔌 Port: {client.PORT if hasattr(client, 'PORT') else '27017'}")

except Exception as e:
    print(f"❌ Failed to connect to MongoDB: {e}")

# Access your database and collection
db = client[MONGO_DB]
print("📚 Collections:", db.list_collection_names())
notes_collection = db["notes"]
users_collection = db["users"]
