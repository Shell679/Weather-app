from fastapi import FastAPI
from app.api.routers.weather_router import router as weather_router
app = FastAPI()

app.include_router(weather_router)