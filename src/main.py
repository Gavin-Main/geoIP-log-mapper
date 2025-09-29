from src.parser import extract_ips_from_log
from src.geolocate import geolocate_ip
from src.visualize import create_map

def main():
    log_file = "logs/sample.log"
    db_path = "geoip2-db/GeoLite2-City.mmdb"

    ips = extract_ips_from_log(log_file)
    locations = []

    for ip in ips:
        loc = geolocate_ip(ip, db_path)
        locations.append(loc)

    create_map(locations)

if __name__ == "__main__":
    main()
