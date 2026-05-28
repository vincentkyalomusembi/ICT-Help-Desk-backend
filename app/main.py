from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.database import check_db_connection
from app.routes import auth_router
from app.routes import audit_router
from app.routes import assets_router
from app.routes import assets_admin_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await check_db_connection()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(audit_router)
app.include_router(assets_router)
app.include_router(assets_admin_router)

@app.get("/")
async def home():
    return {"message": "Hello, World!"}
