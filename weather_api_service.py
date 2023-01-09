"""Get weather from web-service"""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import requests

from gps_coordinates import Coordinates
from exceptions import DontGetWeather


API_KEY = "YOUR_OPENWEATHER_API_KEY"
OPENWEATHER_API_URL = (
    "https://api.openweathermap.org/data/2.5/weather?"
    "lat={latitude}&lon={longitude}&"
    "&units=metric&lang=ru&"
    "appid=" + API_KEY
)

Celsius = int


class WeatherType(Enum):
    """Enum for weather type"""
    THUNDERSTORM = "Гроза"
    DRIZZLE = "Изморозь"
    RAIN = "Дождь"
    SNOW = "Снег"
    FOG = "Туман"
    CLEAR = "Ясно"
    CLOUDS = "Облачно"


@dataclass
class Weather:
    """Weather dataclass"""
    city: str
    temperature: Celsius
    feels_like: Celsius
    weather_type: WeatherType
    sunrise: datetime
    sunset: datetime


def get_weather(coordinates: Coordinates) -> Weather:
    """Returns Weather info by GPS coordinates"""
    weater_data = _get_weather_data(coordinates)
    try:
        weather = _parse_weather(weater_data)
    except Exception as exc:
        raise DontGetWeather from exc
    return weather


def _get_weather_data(coordinates: Coordinates) -> dict:
    response = requests.get(
        OPENWEATHER_API_URL.format(
            latitude=coordinates.latitude,
            longitude=coordinates.longitude,
        ),
        timeout=200
    )
    if response.status_code == 200:
        return response.json()
    else:
        raise DontGetWeather


def _parse_weather(weather_data: dict) -> Weather:
    return Weather(
        city=weather_data["name"],
        temperature=Celsius(weather_data["main"]["temp"]),
        weather_type=_parse_weather_type(
            str(weather_data["weather"][0]["id"])),
        feels_like=Celsius(weather_data["main"]["feels_like"]),
        sunrise=datetime.fromtimestamp(weather_data["sys"]["sunrise"]),
        sunset=datetime.fromtimestamp(weather_data["sys"]["sunset"])
    )


def _parse_weather_type(weather_type_id: str) -> WeatherType:
    weather_type = {
        "2": WeatherType.THUNDERSTORM,
        "3": WeatherType.DRIZZLE,
        "5": WeatherType.RAIN,
        "6": WeatherType.SNOW,
        "7": WeatherType.FOG,
        "800": WeatherType.CLEAR,
        "80": WeatherType.CLOUDS
    }

    for weather_key, weather_type in weather_type.items():
        if weather_type_id.startswith(weather_key):
            return weather_type

    raise DontGetWeather


if __name__ == "__main__":
    print(get_weather(Coordinates(55.75, 37.61)))
