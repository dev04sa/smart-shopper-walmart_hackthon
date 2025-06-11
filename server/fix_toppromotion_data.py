import pymongo
import pandas as pd
from bson.binary import Binary
import requests
from io import BytesIO
from search_result import search_result

# MongoDB setup
client = pymongo.MongoClient("mongodb+srv://devsa2067:H4q4Gveoi3oc9NhY@cluster0.rblzmli.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["mydatabase"]
collection = db["mycollection"]
search_history = db["searchHistory"]

# Load article CSV
df = pd.read_csv("articles.csv")
article_dict = df.set_index("article_id").to_dict("index")

# Image URLs you provided (cycling through them)
image_urls = [
    "https://www.aaramkhor.com/cdn/shop/products/Black-1_1000x.jpg",  # Replaced with actual image URL from page
    "https://thebanyantee.com/cdn/shop/files/Black-T-shirt.jpg?v=1721380366",
    "https://www.jiomart.com/images/product/original/rvwqhtn7pt/t-shirt-product-images-orvwqhtn7pt-p597677946-0-202303060712.jpg"
]

# Pre-download images and cycle through them
downloaded_images = []
for url in image_urls:
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            downloaded_images.append(Binary(response.content))
            print(f"✅ Downloaded image from {url}")
        else:
            print(f"⚠️ Failed to download {url}")
    except Exception as e:
        print(f"❌ Error downloading {url}: {e}")

if not downloaded_images:
    print("🚨 No images downloaded. Using dummy fallback.")
    downloaded_images = [Binary(b"This is dummy image data")]

# Begin data insertion
inserted_count = 0
image_index = 0

all_users = search_history.find()

for user in all_users:
    user_id = user["user_id"]
    search_string = user["search_string"]

    results = search_result(search_string, 3)

    for aid in results:
        aid = int(aid)
        exists = collection.find_one({"article_id": aid})
        if not exists:
            if aid in article_dict:
                doc = article_dict[aid]
                doc["article_id"] = aid
                doc["image"] = downloaded_images[image_index % len(downloaded_images)]
                image_index += 1
                collection.insert_one(doc)
                inserted_count += 1
                print(f"✅ Inserted article {aid} with image {image_index % len(downloaded_images)}")
            else:
                print(f"❌ Article ID {aid} not found in CSV")

print(f"\n🚀 Completed. Total new articles inserted: {inserted_count}")
