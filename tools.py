def calculate_spn(toponym: dict) -> str:
    envelope = toponym["boundedBy"]["Envelope"]
    lower_corner = envelope["lowerCorner"].split()
    upper_corner = envelope["upperCorner"].split()

    delta_lon = str(abs(float(upper_corner[0]) - float(lower_corner[0])))
    delta_lat = str(abs(float(upper_corner[1]) - float(lower_corner[1])))
    
    return delta_lon, delta_lat
    

def get_map_params(toponym: dict) -> dict:
    toponym_coordinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_latitude = toponym_coordinates.split(" ")
    
    delta_lon, delta_lat = calculate_spn(toponym)
    
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_latitude]),
        "spn": ",".join([delta_lon, delta_lat]),
        "l": "map",
        "pt": ",".join([toponym_longitude, toponym_latitude, "pm2rdl"])
    }
    
    return map_params
