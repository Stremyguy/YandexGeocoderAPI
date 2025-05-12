import sys
import requests
from io import BytesIO
from PIL import Image
from geocoder import geocode
from organizations import find_organizations
from map_utils import get_map_params
from distance import calculate_distance


def get_pharmacy_marker(pharmacy: dict) -> str:
    try:
        company_meta = pharmacy["properties"]["CompanyMetaData"]
        hours = company_meta.get("Hours")
        
        if not hours:
            return "pm2grm"
        
        availabilities = hours.get("Availabilities", [])
        if availabilities:
            for av in availabilities:
                if av.get("TwentyFourHours"):
                    return "pm2gnm"
        
        return "pm2blm"
    
    except Exception:
        return "pm2grm"


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python main.py 'address'")
        return
    
    address = " ".join(sys.argv[1:])
    
    GEOCODER_API_KEY = "8013b162-6b42-4997-9691-77b7074026e0"
    SEARCH_API_KEY = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    STATIC_MAPS_API_KEY = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"

    try:
        address_coords = geocode(address, GEOCODER_API_KEY)
        
        if not (-180 <= address_coords[0] <= 180 and -90 <= address_coords[1] <= 90):
            raise ValueError("Invalid coordinates received from geocoder")
        
        address_point = f"{address_coords[0]},{address_coords[1]},pm2rdl"
        
        pharmacies = find_organizations(SEARCH_API_KEY, "аптека", address_coords)
        
        points = [address_point]
        min_lon, max_lon = address_coords[0], address_coords[0]
        min_lat, max_lat = address_coords[1], address_coords[1]
        
        print("\nНайденные аптеки:")
        for i, pharmacy in enumerate(pharmacies, 1):
            name = pharmacy["properties"]["CompanyMetaData"]["name"]
            ph_address = pharmacy["properties"]["CompanyMetaData"]["address"]
            hours = pharmacy["properties"]["CompanyMetaData"].get("Hours", {}).get("text", "Время работы не указано")
            
            ph_coords = pharmacy["geometry"]["coordinates"]
            marker = get_pharmacy_marker(pharmacy)
            ph_point = f"{ph_coords[0]},{ph_coords[1]},{marker}"  # Fixed typo: marker -> marker
            points.append(ph_point)
            
            min_lon = min(min_lon, ph_coords[0])
            max_lon = max(max_lon, ph_coords[0])
            min_lat = min(min_lat, ph_coords[1])
            max_lat = max(max_lat, ph_coords[1])
            
            distance = calculate_distance(address_coords, ph_coords)
        
            print(f"\n{i}. {name}")
            print(f"    Адрес: {ph_address}")
            print(f"    Время работы: {hours}")
            print(f"    Расстояние от указанного адреса: {distance:.2f} км")
        
        center = [
            (min_lon + max_lon) / 2,
            (min_lat + max_lat) / 2
        ]
        
        delta_lon = abs(max_lon - min_lon) * 1.2
        delta_lat = abs(max_lat - min_lat) * 1.2
        
        if delta_lat > 90 or delta_lon > 180:
            print("Ошибка: Слишком большой охват карты")
            print(f"Полученные значения: долгота={delta_lon}, широта={delta_lat}")
            return
        
        map_params = get_map_params(center, points, (delta_lon, delta_lat))
        map_params["apikey"] = STATIC_MAPS_API_KEY
        
        map_api_server = "https://static-maps.yandex.ru/v1"
        response = requests.get(map_api_server, params=map_params)
        response.raise_for_status()
        
        im = BytesIO(response.content)
        opened_image = Image.open(im)
        opened_image.show()
        
    except requests.exceptions.HTTPError as e:
        print(f"Ошибка HTTP: {e}")
        if e.response.status_code == 400:
            print("Возможные причины:")
            print("- Неверные параметры запроса (проверьте координаты)")
            print("- Запрос выходит за пределы покрытия карт")
            print(f"URL запроса: {e.response.url}")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()