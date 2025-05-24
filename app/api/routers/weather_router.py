from fastapi import APIRouter, Query

from app.api.services.weather_geocoding import get_coordinates
from app.api.services.weather_service import get_daily_weather
from app.schemas.schemas import WeatherResponse

router = APIRouter(
    tags=["Weather"],
    prefix="/api"
)

@router.get("/weather", response_model=WeatherResponse)
async def get_weather_by_city(request_city: str = Query()):
    coordinates = await get_coordinates(request_city)

    weather_data = await get_daily_weather(*coordinates)
    return weather_data