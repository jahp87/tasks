import os
import aiohttp
from fastapi import Request, Depends
from sqlalchemy.orm import Session
from functools import wraps
from .models import ApiCallLog
from .database import get_db

WEATHERAPI_KEY =   os.getenv('WEATHERAPI_KEY', 'a0e1e9718d3f485ea70193609242209')

def log_ip_country_weather(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get('request')
        db: Session = kwargs.get('db')

        if not request or not db:
            raise Exception("Request and DB session are required")

        ip_address = request.client.host
        if(ip_address == 'localhost' or ip_address=='127.0.0.1'):
            ip_address = '169.150.218.27'

        # Get Country from IP using a free geolocation API (ip-api.com)
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://ip-api.com/json/{ip_address}") as response:
                geo_data = await response.json()
                country = geo_data.get("country", "Unknown")
                print(country)

        # Get Weather using WeatherAPI
        async with aiohttp.ClientSession() as session:
            weather_url = f"http://api.weatherapi.com/v1/current.json?key={WEATHERAPI_KEY}&q={country}"
            async with session.get(weather_url) as response:
                weather_data = await response.json()
                weather_state = weather_data.get('current', {}).get('condition', {}).get('text', 'Unknown')

  
        log_entry = ApiCallLog(ip_address=ip_address, country=country, weather_state=weather_state)
        db.add(log_entry)
        db.commit()


        return await func(*args, **kwargs)

    return wrapper
