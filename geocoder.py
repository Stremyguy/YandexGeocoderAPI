import requests


def geocode(address: str, apikey: str) -> list:
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    
    geocoder_params = {
        "apikey": apikey,
        "geocode": address,
        "format": "json"
    }
    
    response = requests.get(geocoder_api_server, params=geocoder_params)
    response.raise_for_status()
    
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    pos = toponym["Point"]["pos"]
    
    return list(map(float, pos.split()))
