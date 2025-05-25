from datetime import datetime

from pydantic import BaseModel


class WeatherResponse(BaseModel):
    current_temperature: float
    forecast: list