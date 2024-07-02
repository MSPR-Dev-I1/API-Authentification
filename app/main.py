import os
from fastapi import FastAPI
from app.routers import auth
from app.database.premier_schema import setup_database
from app.messages.subscription import lifespan

app = FastAPI(lifespan=lifespan)


origins = ["*"]


app.include_router(auth.router, prefix="/authentification")

if os.getenv("RUNNING_WITH_UVICORN"):
    setup_database()
