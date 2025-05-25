from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.weather_router import router as weather_router
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(weather_router)