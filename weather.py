from gps_coordinates import get_gps_coordinates
from weather_api_service import get_weather
from weather_formatter import format_weather
from exceptions import DontGetCoordinates, DontGetWeather


def main():
    """Main app func"""
    try:
        coordinates = get_gps_coordinates()
        weather = get_weather(coordinates)
        print(format_weather(weather))
    except DontGetWeather:
        print("Возникла ошибка при получении погоды")
    except DontGetCoordinates:
        print("Возникла ошибка при определении GPS-координат")


if __name__ == "__main__":
    main()
