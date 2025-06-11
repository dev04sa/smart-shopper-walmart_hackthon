import bson
from pymongo import MongoClient

# === Step 1: Read BSON file ===
bson_file_path = 'mydatabase/mydatabase/mycollection.bson'
documents = []

with open(bson_file_path, 'rb') as f:
    data = bson.decode_file_iter(f)
    for doc in data:
        documents.append(doc)

print(f"✅ Loaded {len(documents)} documents from BSON.")

# === Step 2: Connect to MongoDB Atlas ===
# Replace these with your MongoDB Atlas credentials
MONGO_URI = "mongodb+srv://devsa2067:H4q4Gveoi3oc9NhY@cluster0.rblzmli.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)

db_name = "mydatabase"           # e.g. "test"
collection_name = "mycollection"

db = client[db_name]
collection = db[collection_name]

# === Step 3: Insert Documents ===
if documents:
    result = collection.insert_many(documents)
    print(f"🎉 Successfully inserted {len(result.inserted_ids)} documents into '{collection_name}' collection.")
else:
    print("⚠️ No documents to insert.")
