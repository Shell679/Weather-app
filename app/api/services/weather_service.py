from datetime import datetime

import httpx

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
    async with httpx.AsyncClient() as client:
        response_daily = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "daily": "temperature_2m_max,precipitation_sum,weathercode",
                "timezone": "auto"
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

        data_hourly = response_hourly.json()
        now = datetime.now().hour
        data_daily = response_daily.json()

        current_temp = data_hourly["hourly"]["temperature_2m"][now]
        max_temp = data_daily["daily"]["temperature_2m_max"][0]
        weather_code = data_daily["daily"]["weathercode"][0]
        precipitation = data_daily["daily"]["precipitation_sum"][0]
        time = data_daily["daily"]["time"][0]

        verdict = WEATHER_CODE_DESCRIPTIONS.get(weather_code, "Неизвестно")

        return {
            "current_temperature": current_temp,
            "max_temperature": max_temp,
            "precipitation": precipitation,
            "verdict": verdict,
            "time": time,
        }