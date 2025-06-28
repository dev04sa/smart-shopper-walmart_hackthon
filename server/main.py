# # main.py

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware.wsgi import WSGIMiddleware

# # Import your FastAPI router
# from routers import tryon

# # Import your Flask app
# from app import app as flask_app

# # Create FastAPI app
# app = FastAPI()

# # Enable CORS for frontend access
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Set specific domains in production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Mount Flask app under /flask or root
# app.mount("/", WSGIMiddleware(flask_app))  # Mount Flask at root
# # You can change to "/flask" if you want to isolate it: app.mount("/flask", WSGIMiddleware(flask_app))

# # Mount FastAPI routers
# app.include_router(tryon.router, prefix="/api")



from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.wsgi import WSGIMiddleware
from starlette.routing import Mount, Router
from routers import tryon
from app import app as flask_app  # Your Flask app

from starlette.applications import Starlette

# Create your main FastAPI app
fastapi_app = FastAPI()

# Mount your FastAPI routers
fastapi_app.include_router(tryon.router, prefix="/api")

# Add CORS middleware (if needed)
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a new ASGI app that routes:
# /api/* => FastAPI
# everything else => Flask
application = Starlette(
    routes=[
        Mount("/api", app=fastapi_app),  # route FastAPI under /api
        Mount("/", app=WSGIMiddleware(flask_app)),  # fallback to Flask for everything else
    ]
)

