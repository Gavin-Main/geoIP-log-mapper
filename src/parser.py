import re

def extract_ips_from_log(log_path):
    ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    unique_ips = set()

    with open(log_path, 'r') as file:
        for line in file:
            match = ip_pattern.search(line)
            if match:
                unique_ips.add(match.group())

    return list(unique_ips)

# For testing
if __name__ == "__main__":
    log_file = "/logs/Apache_2k.log"
    ips = extract_ips_from_log(log_file)
    print(f"Found {len(ips)} unique IPs:")
    print(ips)

