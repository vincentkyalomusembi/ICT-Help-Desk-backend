from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.database import check_db_connection
from app.routes import auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await check_db_connection()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)