from fastapi import FastAPI

from app.routes.devices import router


app = FastAPI(title="NetPulse", description="In-memory network device monitoring API")
app.include_router(router)