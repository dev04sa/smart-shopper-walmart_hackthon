import pandas as pd
import pymongo
import base64
import os
from bson.binary import Binary

# ==== CONFIGURATION ====
MONGO_URI = "mongodb+srv://devsa2067:H4q4Gveoi3oc9NhY@cluster0.rblzmli.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "mydatabase"
COLLECTION_NAME = "mycollection"
CSV_PATH = "articles.csv"  # Make sure this file is in the same folder
NUM_RECORDS = 10000        # Match your recommender setup
# ========================

def load_articles(csv_path, limit):
    print("📥 Loading CSV...")
    df = pd.read_csv(csv_path)
    return df[:limit]  # Take top 10k for consistency

def connect_mongodb(uri, db_name, collection_name):
    print("🔌 Connecting to MongoDB...")
    client = pymongo.MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]
    return collection

def insert_articles(collection, articles_df):
    print("📦 Preparing dummy image...")
    dummy_image_binary = Binary(base64.b64decode(base64.b64encode(b'This is dummy image data')))

    print(f"📤 Inserting {len(articles_df)} articles into MongoDB...")
    inserted = 0
    for _, row in articles_df.iterrows():
        doc = row.to_dict()
        doc["image"] = dummy_image_binary
        try:
            collection.insert_one(doc)
            inserted += 1
        except Exception as e:
            print(f"❌ Failed to insert article_id={doc.get('article_id')}: {e}")
    print(f"✅ Inserted {inserted} articles successfully.")

if __name__ == "__main__":
    try:
        articles_df = load_articles(CSV_PATH, NUM_RECORDS)
        collection = connect_mongodb(MONGO_URI, DB_NAME, COLLECTION_NAME)
        insert_articles(collection, articles_df)
    except Exception as e:
        print(f"🔥 Script error: {e}")
