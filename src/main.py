import geoip2.database
from pathlib import Path
from parser import extract_ips_from_log
from geolocate import geolocate_ip
from visualize import create_map

def main():

    # Get project's root directory
    project_root = Path(__file__).resolve().parent.parent

    # Define paths relative to project root.
    log_file = project_root / "logs" / "fabricated_apache_access.log"
    db_path = project_root / "geoip2-db" / "GeoLite2-City.mmdb"
    output_path = project_root / "output" / "ip_map.html"

    # Verify required files exist before processing
    if not log_file.is_file():
        print(f"Error: Log file not found: {log_file}")
        return

    if not db_path.is_file():
        print(f"Error: GeoIP database not found: {db_path}")
        return

    # Extract IP addresses from the log file
    ips = extract_ips_from_log(str(log_file))
    print(f"Extracted {len(ips)} IP addresses.")

    # Geolocate each extracted IP address
    locations = []

    # Open the GeoIP database once for all lookups.
    with geoip2.database.Reader(str(db_path)) as reader:
        for ip in ips:
            loc = geolocate_ip(ip, reader=reader)

            if "error" not in loc:
                locations.append(loc)
            else:
                print(f"Skipped {ip}: {loc['error']}")

    # Generate an offline-viewable HTML map
    create_map(locations, str(output_path))

    print("GeoIP mapping completed successfully.")

if __name__ == "__main__":
    main()
