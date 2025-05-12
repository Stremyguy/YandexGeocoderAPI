import requests


def find_organizations(api_key: str, query: str, coordinates: list, count: int = 10) -> str:
    search_api_server = "https://search-maps.yandex.ru/v1/"
    address_ll = f"{coordinates[0]},{coordinates[1]}"
    
    search_params = {
        "apikey": api_key,
        "text": query,
        "lang": "ru-RU",
        "ll": address_ll,
        "type": "biz",
        "results": count
    }
    
    response = requests.get(search_api_server, params=search_params)
    response.raise_for_status()
    
    return response.json()["features"]
