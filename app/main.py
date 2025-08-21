from fastapi import FastAPI
from app.api.v1 import users

app = FastAPI(title="Secretly API")

app.include_router(users.router, prefix="/api/v1/users", tags=["users"])