import requests

from io import BytesIO
from PIL import Image
from tools import get_coordinates, calculate_distance, get_map_params


def main() -> None:
    address = input()

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "geocode": address,
        "format": "json"
    }

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        pass

    try:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        address_coords = get_coordinates(toponym)
        address_ll = f"{address_coords[0]},{address_coords[1]}"
    except Exception as e:
        print(f"Не найдено результатов по запросу: {address}")

    search_api_server = "https://search-maps.yandex.ru/v1/"
    search_params = {
        "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
        "text": "аптека",
        "lang": "ru_RU",
        "ll": address_ll,
        "type": "biz",
        "results": 1
    }
    
    response = requests.get(search_api_server, params=search_params)
    
    if not response:
        return
    
    try:
        json_response = response.json()
        pharmacy = json_response["features"][0]
        
        name = pharmacy["properties"]["CompanyMetaData"]["name"]
        ph_address = pharmacy["properties"]["CompanyMetaData"]["address"]
        hours = pharmacy["properties"]["CompanyMetaData"].get("Hours", {}).get("text", "Время работы не указано")
        
        ph_coords = pharmacy["geometry"]["coordinates"]
        ph_point = f"{ph_coords[0]},{ph_coords[1]},pm2gnl"
        
        distance = calculate_distance(address_coords, ph_coords)
        
        print("\nНайденная аптека:")
        print(f"Название: {name}")
        print(f"Адрес: {ph_address}")
        print(f"Время работы: {hours}")
        print(f"Расстояние от указанного адреса: {distance:.2f} км")
        
        address_point = f"{address_coords[0]},{address_coords[1]},pm2rdl"
        points = [address_point, ph_point]
        
        center = [
            (address_coords[0] + ph_coords[0]) / 2,
            (address_coords[1] + ph_coords[1]) / 2,
        ]
        
        delta_lon = abs(address_coords[0] - ph_coords[0]) * 1.5
        delta_lat = abs(address_coords[1] - ph_coords[1]) * 1.5
        spn = (delta_lon, delta_lat)
    
        map_params = get_map_params(center, points, spn)
        map_api_server = "https://static-maps.yandex.ru/v1"
        response = requests.get(map_api_server, params=map_params)
        
        if not response:
            return
        
        im = BytesIO(response.content)
        opened_image = Image.open(im)
        opened_image.show()
    except Exception as e:
        print(f"Ошибка: {e}")
        return


if __name__ == "__main__":
    main()
