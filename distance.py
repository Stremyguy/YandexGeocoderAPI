from math import radians, sin, cos, sqrt, atan2


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
