from flask import *
from bson import ObjectId
import jwt
import pymongo
myclient = pymongo.MongoClient("mongodb+srv://devsa2067:H4q4Gveoi3oc9NhY@cluster0.rblzmli.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
mydb = myclient['mydatabase']
collection = mydb['users']

class AuthenticationMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # Extract the authorization token from the 'Authorization' header :-
        authorization_header = environ.get('HTTP_AUTHORIZATION')
        if authorization_header:
            token = authorization_header
            user = jwt.decode(token, "SignedByRK", algorithms="HS256")
            id = ObjectId(user['id'])
            user = collection.find_one({"_id": id})
            if(user):
                user.pop("password") # Remove password before sending user details to the endpoint
                environ['user'] = user
                return self.app(environ, start_response)
            else:
                # Handle unauthorized access
                res = Response(u'Authorization failed', mimetype= 'text/plain', status=401)
                return res(environ, start_response)
        
        return self.app(environ, start_response)