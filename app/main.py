from fastapi import FastAPI
from app.routers import auth

app = FastAPI()


origins = ["*"]


app.include_router(auth.router, prefix="/authentification")
