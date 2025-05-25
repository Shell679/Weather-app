from fastapi import HTTPException

import httpx


async def get_coordinates(city: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": city, "format": "json", "limit": 1}
        )

        if response.status_code != 200:
            raise HTTPException(status_code=503, detail="Сервис геолокации временно недоступен")

        data = response.json()
        if not data:
            raise HTTPException(status_code=404, detail="Данный город не найден")
        try:
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
        except (KeyError, ValueError):
            raise HTTPException(status_code=500, detail="Ошибка обработки координат")

        return lat, lon
