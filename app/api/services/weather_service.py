from datetime import datetime, timedelta

import httpx
from fastapi import HTTPException

WEATHER_CODE_DESCRIPTIONS = {
    0: "Ясно",
    1: "Преимущественно ясно",
    2: "Переменная облачность",
    3: "Пасмурно",
    45: "Туман",
    48: "Изморозь",
    51: "Лёгкая морось",
    61: "Слабый дождь",
    63: "Умеренный дождь",
    65: "Сильный дождь",
    71: "Снег",
    80: "Слабый ливень",
    81: "Ливень",
    82: "Сильный ливень",
    95: "Гроза",
}

async def get_daily_weather(lat: float, lon: float):
    today = datetime.utcnow().date()
    end_day = today + timedelta(days=6)

    async with httpx.AsyncClient() as client:
        # Прогноз по дням
        response_daily = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode",
                "timezone": "auto",
                "start_date": today.isoformat(),
                "end_date": end_day.isoformat()
            }
        )

        response_hourly = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "hourly": "temperature_2m",
                "timezone": "auto"
            }
        )

    if response_daily.status_code != 200 or response_hourly.status_code != 200:
        raise HTTPException(status_code=503, detail="Сервис погоды временно недоступен")

    data_daily = response_daily.json()
    data_hourly = response_hourly.json()

    try:
        now = datetime.now().hour
        current_temp = data_hourly["hourly"]["temperature_2m"][now]

        temps_max = data_daily["daily"]["temperature_2m_max"]
        temps_min = data_daily["daily"]["temperature_2m_min"]
        codes = data_daily["daily"]["weathercode"]
        precs = data_daily["daily"]["precipitation_sum"]
        times = data_daily["daily"]["time"]
    except KeyError:
        raise HTTPException(status_code=500, detail="Ошибка при разборе погодных данных")

    forecast = []
    for i in range(len(times)):
        verdict = WEATHER_CODE_DESCRIPTIONS.get(codes[i], "Неизвестно")
        forecast.append({
            "date": times[i],
            "temperature_max": temps_max[i],
            "temperature_min": temps_min[i],
            "precipitation": precs[i],
            "verdict": verdict
        })

    return {
        "current_temperature": current_temp,
        "forecast": forecast
    }