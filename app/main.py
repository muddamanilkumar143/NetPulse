from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import STORAGE_BACKEND
from app.db.collections import ensure_indexes
from app.db.mongo import close_client, get_db
from app.routes.devices import router


@asynccontextmanager
async def lifespan(app: FastAPI):
	try:
		if STORAGE_BACKEND == "mongo":
			ensure_indexes(get_db())
		yield
	finally:
		if STORAGE_BACKEND == "mongo":
			close_client()


app = FastAPI(
	title="NetPulse",
	description="Network device monitoring API",
	lifespan=lifespan,
)
app.include_router(router)