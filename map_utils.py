from math import radians, sin, cos, sqrt, atan2


def calculate_spn(toponym: dict) -> str:
    envelope = toponym["boundedBy"]["Envelope"]
    lower_corner = envelope["lowerCorner"].split()
    upper_corner = envelope["upperCorner"].split()

    delta_lon = str(abs(float(upper_corner[0]) - float(lower_corner[0])))
    delta_lat = str(abs(float(upper_corner[1]) - float(lower_corner[1])))
    
    return delta_lon, delta_lat


def get_map_params(center: list, points: list, spn=None) -> dict:
    map_params = {
        "ll": f"{center[0]},{center[1]}",
        "l": "map",
        "pt": "~".join(points)
    }
    
    if spn:
        map_params["spn"] = f"{spn[0]},{spn[1]}"
    
    return map_params
