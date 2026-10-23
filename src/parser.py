import re
import ipaddress
from pathlib import Path

# Extract unique, valid IPv4 addresses from Apache access 
# logs. Returns a list of unique IP address strings.

def extract_ips_from_log(log_path):

    # Match an IPv4 address at the beginning of a log line.
    ip_pattern = re.compile(r"^\s*(\d{1,3}(?:\.\d{1,3}){3})(?=\s)")

    unique_ips = set()

    # Read the log file one line at a time.
    with open(log_path, "r", encoding="utf-8", errors="replace") as file:
        for line in file:
            match = ip_pattern.search(line)

            if match:
                ip = match.group(1)

                # Validate the extracted IP address.
                try:
                    ip_obj = ipaddress.ip_address(ip)

                    # Only accept valid IPv4 addresses.
                    if isinstance(ip_obj, ipaddress.IPv4Address):
                        unique_ips.add(ip)

                except ValueError:
                    
                    # Ignore invalid IP addresses.
                    continue

    # Return a consistent, sorted list.
    return sorted(unique_ips)


# Run independently to test IP extraction.
if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    log_file = project_root / "logs" / "Apache_2k.log"

    ips = extract_ips_from_log(log_file)

    print(f"Found {len(ips)} unique IPs:")

    for ip in ips:
        print(ip)
