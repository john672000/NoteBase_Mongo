from pymongo import MongoClient
from dotenv import load_dotenv
import os
import urllib.parse
import certifi

load_dotenv()

# Get the MongoDB URI from environment variables
MONGO_URI = os.getenv("MONGO_URI")
print(f'Environment set URI = {MONGO_URI}')
MONGO_DB = "test"

try:
    # Configure MongoDB client with explicit SSL settings
    client = MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=5000,
        ssl=True,
        tlsCAFile=certifi.where(),  # Use certifi's CA bundle
        retryWrites=True,
        w="majority",
        tls=True,
        tlsAllowInvalidCertificates=False
    )
    
    # Test connection
    client.admin.command("ping")
    print(f"✅ Connected to MongoDB at {MONGO_URI}")
    print(f"📂 Using database: {MONGO_DB}")
    print(f"🔌 Port: {client.PORT if hasattr(client, 'PORT') else '27017'}")

except Exception as e:
    print(f"❌ Failed to connect to MongoDB: {e}")
    raise  # Re-raise the exception to ensure the app fails if DB connection fails

# Access your database and collection
db = client[MONGO_DB]
print("📚 Collections:", db.list_collection_names())
notes_collection = db["notes"]
users_collection = db["users"]