import requests

from io import BytesIO
from PIL import Image
from tools import get_map_params


def main() -> None:
    print("Введите название локации:")
    toponym_to_find = input()

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        pass

    json_response = response.json()

    try:
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    except Exception as e:
        print(f"Не найдено результатов по запросу: {toponym_to_find}")
    
    map_params = get_map_params(toponym)
    map_params["apikey"] = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"

    map_api_server = "https://static-maps.yandex.ru/v1"
    response = requests.get(map_api_server, params=map_params)
    
    if not response:
        return
    
    im = BytesIO(response.content)
    opened_image = Image.open(im)
    opened_image.show()


if __name__ == "__main__":
    main()