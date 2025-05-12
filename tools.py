from math import radians, sin, cos, sqrt, atan2


def calculate_spn(toponym: dict) -> str:
    envelope = toponym["boundedBy"]["Envelope"]
    lower_corner = envelope["lowerCorner"].split()
    upper_corner = envelope["upperCorner"].split()

    delta_lon = str(abs(float(upper_corner[0]) - float(lower_corner[0])))
    delta_lat = str(abs(float(upper_corner[1]) - float(lower_corner[1])))
    
    return delta_lon, delta_lat


def get_coordinates(toponym: str) -> list:
    pos = toponym["Point"]["pos"]
    return list(map(float, pos.split()))


def calculate_distance(point1: list, point2: list) -> float:
    lat1, lon1 = point1
    lat2, lon2 = point2

    R = 6371
    
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    
    a = (sin(dlat / 2) * sin(dlat / 2) +
         cos(radians(lat1)) * cos(radians(lat2)) *
         sin(dlon / 2) * sin(dlon / 2))
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    return R * c


def get_map_params(center: list, points: list, spn=None) -> dict:
    map_params = {
        "ll": f"{center[0]},{center[1]}",
        "l": "map",
        "apikey": "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13",
        "pt": "~".join(points)
    }
    
    if spn:
        map_params["spn"] = f"{spn[0]},{spn[1]}"
    
    return map_params
