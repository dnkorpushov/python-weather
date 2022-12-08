"""Get GPS coordinates by your computer's ip-address"""
from typing import NamedTuple
import requests
from exceptions import DontGetCoordinates

IPINFO_URL = 'https://ipinfo.io/json'


class Coordinates(NamedTuple):
    """Class for GPS Coordinates"""
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
    except Exception as exc:
        raise DontGetCoordinates from exc
    return Coordinates(latitude=latitude, longitude=longitude)


def _get_location_info_by_ip() -> dict:
    response = requests.get(IPINFO_URL, timeout=200)
    if response.status_code == 200:
        return response.json()
    raise DontGetCoordinates


if __name__ == "__main__":
    print(get_gps_coordinates())
