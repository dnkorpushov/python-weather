import requests
from typing import NamedTuple
from exceptions import DontGetCoordinates

IPINFO_URL = 'https://ipinfo.io/json'


class Coordinates(NamedTuple):
    latitude: float = None
    longitude: float = None


def get_gps_coordinates() -> Coordinates: 
    """Returns GPS coordinates by computer's ip"""
    location_info = _get_location_info_by_ip()
    coordinates = _parse_coordinates(location_info)
    return coordinates


def _parse_coordinates(location_info: dict) -> Coordinates:
    try:
        latitude, longitude = location_info["loc"].split(",")
    except Exception:
        raise DontGetCoordinates
    return Coordinates(latitude=latitude, longitude=longitude)


def _get_location_info_by_ip() -> dict:
    response = requests.get(IPINFO_URL)
    if response.status_code == 200:
        return response.json()
    else:
        raise DontGetCoordinates


if __name__ == "__main__":
    print(get_gps_coordinates())
