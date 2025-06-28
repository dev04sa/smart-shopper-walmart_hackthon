from flask import *
app = Flask(__name__)


# Enable CORS :-
from flask_cors import CORS
CORS(app)

# Calling middleware :-
import middleware.middleware as middleware
app.wsgi_app = middleware.AuthenticationMiddleware(app.wsgi_app)

import pymongo
myclient = pymongo.MongoClient("mongodb+srv://devsa2067:H4q4Gveoi3oc9NhY@cluster0.rblzmli.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0/")
mydb = myclient['mydatabase']
collection = mydb['mycollection']
search_collection = mydb['searchHistory']

import base64

# Register the blueprints :-
import routes.users as users
app.register_blueprint(users.users_bp)

import routes.promotions as promotions
app.register_blueprint(promotions.promotions_bp)

import routes.buy as buy
app.register_blueprint(buy.buy_bp)

import search_result
import recommender

@app.route("/search", methods=['POST'])
def search():
    try:
        searchStr = request.form['searchStr']
        results = search_result.search_result(searchStr, 50)
        if not len(results):
            return {"error": "No products found"}, 400
        results = results.tolist()
        products = []
        for article_id in results:
            product = collection.find_one({"article_id": article_id}, {"_id": 0})
            if product:
                product["image"] = base64.b64encode(product["image"]).decode('utf-8')
                products.append(product)
            else:
                print(article_id, " not found")
        if not len(products):
            return {"error": "No products found"}, 400
        return {"result": products}, 200
    except:
        return {"error": "Server error"}, 500

@app.route("/getitemdetails", methods=['POST'])
def getItemDetails():
    try:
        article_id = request.form['article_id']
        if not article_id:
            return {"error": "No product found"}, 400
        article_id = int(article_id)
        item = collection.find_one({'article_id': article_id}, {'_id': 0})
        if not item:
            return {"error": "No product found"}, 400
        item["image"] = base64.b64encode(item["image"]).decode('utf-8')
        return {"result": item}, 200
    except:
        return {"error": "Server error"}, 500

@app.route("/cheaper", methods=['POST'])
def cheaper():
    try:
        article_id = request.form['article_id']
        if not article_id:
            return {"error": "No product found"}, 400
        article_id = int(article_id)
        givenProduct = collection.find_one({'article_id': article_id}, {'_id': 0})
        items = recommender.recommendations(article_id, 50)
        items = list(items)
        if not len(items):
            return {"error": "No product found"}, 400
        cheaperItems = []
        for item in items:
            item = int(item)
            similar_item = collection.find_one({'article_id': item}, {'_id': 0})
            if similar_item and similar_item['price'] < givenProduct['price']:
                similar_item["image"] = base64.b64encode(similar_item["image"]).decode('utf-8')
                cheaperItems.append(similar_item)
            if len(cheaperItems) >= 8:
                break
        return {"result": cheaperItems}, 200
    except:
        return {"error": "Server error"}, 500

@app.route('/toppromotion')
def toppromotion():
    try:
        user = request.environ['user']
        if not user:
            return {"error": "User not found"}, 400
        search_string = search_collection.find_one({'user_id': user['_id']})
        search_string = search_string['search_string']
        results = search_result.search_result(search_string, 3)
        if not len(results):
            return {"error": "No products found"}, 400
        results = results.tolist()
        products = []
        for article_id in results:
            product = collection.find_one({"article_id": article_id}, {"_id": 0})
            if product:
                product["image"] = base64.b64encode(product["image"]).decode('utf-8')
                products.append(product)
            else:
                print(article_id, " not found")
        if not len(products):
            return {"error": "No products found"}, 400
        return {"result": products}, 200
    except:
        return {"error": "Server error"}, 500

@app.route('/promotion')
def promotion():
    try:
        user = request.environ['user']
        if not user:
            return {"error": "User not found"}, 400
        try:
            search_string = search_collection.find_one({'user_id': user['_id']})
            search_string = search_string['search_string']
            results = search_result.search_result(search_string, 200)
            if not len(results):
                return {"error": "No products found"}, 400
            results = results.tolist()
            products = []
            for article_id in results:
                product = collection.find_one({"article_id": article_id}, {"_id": 0})
                if product:
                    product["image"] = base64.b64encode(product["image"]).decode('utf-8')
                    products.append(product)
                else:
                    print(article_id, " not found")
            if not len(products):
                return {"error": "No products found"}, 400
            return {"result": products}, 200
        except:
            try:
                items = collection.find({}, {'_id': 0}).limit(50)
                products = []
                for item in list(items):
                    item["image"] = base64.b64encode(item["image"]).decode('utf-8')
                    products.append(item)
                return {"result": products}, 200
            except:
                return {"error": "Server error"}, 500
    except:
        return {"error": "Server error"}, 500

if __name__ == "__main__":
    app.run(debug=True, port=8000)








# from fastapi import FastAPI, Request, Form, UploadFile, File, HTTPException
# from fastapi.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.routing import APIRouter
# from starlette.middleware.base import BaseHTTPMiddleware
# import pymongo
# import base64

# # Import external modules (same as in Flask version)
# import search_result
# import recommender
# from routers import tryon

# # ---------------------------
# # Middleware (converted to FastAPI)
# # ---------------------------

# class AuthenticationMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         # Assuming your middleware logic is here, for now it's a dummy placeholder
#         # Replace with your real logic
#         request.state.user = {"_id": "dummy_user_id"}  # Simulating user injection
#         response = await call_next(request)
#         return response

# # ---------------------------
# # MongoDB Setup
# # ---------------------------
# myclient = pymongo.MongoClient("mongodb+srv://devsa2067:H4q4Gveoi3oc9NhY@cluster0.rblzmli.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0/")
# mydb = myclient['mydatabase']
# collection = mydb['mycollection']
# search_collection = mydb['searchHistory']

# # ---------------------------
# # FastAPI App Setup
# # ---------------------------
# app = FastAPI()

# # CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # For frontend integration
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Add custom middleware
# app.add_middleware(AuthenticationMiddleware)

# # Include tryon router
# app.include_router(tryon.router, prefix="/api")

# # ---------------------------
# # Routes (Converted from Flask to FastAPI)
# # ---------------------------

# @app.post("/search")
# async def search(searchStr: str = Form(...)):
#     try:
#         results = search_result.search_result(searchStr, 50)
#         if not len(results):
#             raise HTTPException(status_code=400, detail="No products found")
#         results = results.tolist()
#         products = []
#         for article_id in results:
#             product = collection.find_one({"article_id": article_id}, {"_id": 0})
#             if product:
#                 product["image"] = base64.b64encode(product["image"]).decode('utf-8')
#                 products.append(product)
#         if not products:
#             raise HTTPException(status_code=400, detail="No products found")
#         return {"result": products}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Server error")


# @app.post("/getitemdetails")
# async def get_item_details(article_id: str = Form(...)):
#     try:
#         if not article_id:
#             raise HTTPException(status_code=400, detail="No product found")
#         article_id = int(article_id)
#         item = collection.find_one({'article_id': article_id}, {'_id': 0})
#         if not item:
#             raise HTTPException(status_code=400, detail="No product found")
#         item["image"] = base64.b64encode(item["image"]).decode('utf-8')
#         return {"result": item}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Server error")


# @app.post("/cheaper")
# async def cheaper(article_id: str = Form(...)):
#     try:
#         if not article_id:
#             raise HTTPException(status_code=400, detail="No product found")
#         article_id = int(article_id)
#         givenProduct = collection.find_one({'article_id': article_id}, {'_id': 0})
#         items = recommender.recommendations(article_id, 50)
#         cheaperItems = []
#         for item in list(items):
#             item = int(item)
#             similar_item = collection.find_one({'article_id': item}, {'_id': 0})
#             if similar_item and similar_item['price'] < givenProduct['price']:
#                 similar_item["image"] = base64.b64encode(similar_item["image"]).decode('utf-8')
#                 cheaperItems.append(similar_item)
#             if len(cheaperItems) >= 8:
#                 break
#         return {"result": cheaperItems}
#     except:
#         raise HTTPException(status_code=500, detail="Server error")


# @app.get("/toppromotion")
# async def toppromotion(request: Request):
#     try:
#         user = request.state.user
#         if not user:
#             raise HTTPException(status_code=400, detail="User not found")
#         search_string = search_collection.find_one({'user_id': user['_id']})['search_string']
#         results = search_result.search_result(search_string, 3)
#         products = []
#         for article_id in results.tolist():
#             product = collection.find_one({"article_id": article_id}, {"_id": 0})
#             if product:
#                 product["image"] = base64.b64encode(product["image"]).decode('utf-8')
#                 products.append(product)
#         if not products:
#             raise HTTPException(status_code=400, detail="No products found")
#         return {"result": products}
#     except:
#         raise HTTPException(status_code=500, detail="Server error")


# @app.get("/promotion")
# async def promotion(request: Request):
#     try:
#         user = request.state.user
#         if not user:
#             raise HTTPException(status_code=400, detail="User not found")
#         try:
#             search_string = search_collection.find_one({'user_id': user['_id']})['search_string']
#             results = search_result.search_result(search_string, 200)
#             products = []
#             for article_id in results.tolist():
#                 product = collection.find_one({"article_id": article_id}, {"_id": 0})
#                 if product:
#                     product["image"] = base64.b64encode(product["image"]).decode('utf-8')
#                     products.append(product)
#             if not products:
#                 raise HTTPException(status_code=400, detail="No products found")
#             return {"result": products}
#         except:
#             # Fallback to random 50 products
#             items = collection.find({}, {'_id': 0}).limit(50)
#             products = []
#             for item in list(items):
#                 item["image"] = base64.b64encode(item["image"]).decode('utf-8')
#                 products.append(item)
#             return {"result": products}
#     except:
#         raise HTTPException(status_code=500, detail="Server error")

# # ---------------------------
# # Run (only if executed directly)
# # ---------------------------

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("app:app", port=8000, reload=True)
