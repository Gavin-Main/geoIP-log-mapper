"""
Project: geoIP-log-mapper

File: geolocate.py

Description: Uses the MaxMind GeoLite2 City database to
             retrieve approximate geographic locations
             for valid public IP addresses.

Created by: Gavin Main

Date Finalized: 10/23/26
"""

import geoip2.database
import geoip2.errors
import ipaddress

# Look up an IP address using the local GeoLite2 database.
# Returns a dictionary containing the IP address,
# city, country, latitude, and longitude.
# If geolocation fails, returns a dictionary
# containing the IP address and an error message.

def geolocate_ip(ip, db_path="../geoip2-db/GeoLite2-City.mmdb", reader=None):

    # Validate the IP address.
    try:
        ip_obj = ipaddress.ip_address(ip)
    except ValueError:
        return {"ip": ip, "error": "Invalid IP address"}

    # Private, loopback, and other non-global addresses
    # cannot be reliably mapped to public locations.
    if not ip_obj.is_global:
        return {"ip": ip, "error": "Non-public IP address"}

    # Open the database only if a reader wasn't supplied.
    owns_reader = reader is None

    try:
        if owns_reader:
            reader = geoip2.database.Reader(db_path)

        # Look up the IP address.
        response = reader.city(ip)

        latitude = response.location.latitude
        longitude = response.location.longitude

        # Ensure valid geographic coordinates exist.
        if latitude is None or longitude is None:
            return {
                "ip": ip,
                "error": "No coordinates found"
            }

        return {
            "ip": ip,
            "city": response.city.name or "Unknown",
            "country": response.country.name or "Unknown",
            "latitude": latitude,
            "longitude": longitude
        }

    except geoip2.errors.AddressNotFoundError:
        return {
            "ip": ip,
            "error": "IP address not found in GeoIP database"
        }

    finally:
        
        # Close the reader only if this function opened it.
        if owns_reader and reader is not None:
            reader.close()
