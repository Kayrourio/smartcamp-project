import httpx

BASE_URL = "https://api.open-meteo.com/v1/forecast"


async def fetch_current(lat: float, lng: float) -> dict:
    params = {
        "latitude": lat,
        "longitude": lng,
        "current": "temperature_2m,relative_humidity_2m,precipitation",
        "timezone": "America/Sao_Paulo",
    }
    async with httpx.AsyncClient(timeout=8.0) as client:
        r = await client.get(BASE_URL, params=params)
        r.raise_for_status()
    c = r.json()["current"]
    return {
        "temperature_c": c["temperature_2m"],
        "humidity_pct": c["relative_humidity_2m"],
        "rainfall_mm": c["precipitation"],
    }


async def fetch_grid(coords: list[tuple[float, float]]) -> list[dict]:
    lats = ",".join(str(lat) for lat, _ in coords)
    lngs = ",".join(str(lng) for _, lng in coords)
    params = {
        "latitude": lats,
        "longitude": lngs,
        "current": "precipitation",
        "timezone": "America/Sao_Paulo",
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.get(BASE_URL, params=params)
        r.raise_for_status()

    results = r.json()
    if isinstance(results, dict):
        results = [results]

    return [
        {
            "lat": coords[i][0],
            "lng": coords[i][1],
            "rainfall_mm": res["current"]["precipitation"],
        }
        for i, res in enumerate(results)
    ]
