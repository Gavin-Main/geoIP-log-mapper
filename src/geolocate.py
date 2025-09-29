import geoip2.database

def geolocate_ip(ip, db_path="../geoip2-db/GeoLite2-City.mmdb"):
    try:
        reader = geoip2.database.Reader(db_path)
        response = reader.city(ip)
        if response.location.latitude is None or response.location.longitude is None:
            return {"ip": ip, "error": "No coordinates found"}
        return {
            "ip": ip,
            "city": response.city.name,
            "country": response.country.name,
            "latitude": response.location.latitude,
            "longitude": response.location.longitude
        }
    except Exception as e:
        return {"ip": ip, "error": str(e)}

