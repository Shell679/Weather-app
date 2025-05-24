from datetime import datetime

from pydantic import BaseModel


class WeatherResponse(BaseModel):
    current_temperature: float
    max_temperature: float
    precipitation: float
    verdict: str
    time: datetime