"""Format Weather class to string"""
from datetime import datetime
from weather_api_service import Weather, WeatherType


def format_weather(weather: Weather) -> str:
    """Returns formatted string from Weather class"""
    return (
        f"{weather.city}:\n"
        f"    температура {weather.temperature} °C, "
        f"ощущается как {weather.feels_like} °C\n"
        f"    {weather.weather_type.value}\n"
        f"    Восход: {weather.sunrise.strftime('%d.%m.%Y %H:%M:%S')}\n"
        f"    Закат: {weather.sunset.strftime('%d.%m.%Y %H:%M:%S')}\n\n"
    )


if __name__ == '__main__':
    print(format_weather(
        Weather(
            city="Moscow",
            temperature=-10,
            feels_like=-15,
            weather_type=WeatherType.CLEAR,
            sunrise=datetime.fromisoformat("2022-12-15 10:05:15"),
            sunset=datetime.fromisoformat("2022-12-15 17:10:20")
        )
    ))
