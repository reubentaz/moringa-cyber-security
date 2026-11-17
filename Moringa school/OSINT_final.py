import os
import json
import socket
import argparse
from datetime import datetime
import whois
import shodan


def get_domain_ip(domain):
    """Resolves a domain name to its primary IP address."""
    try:
        ip_address = socket.gethostbyname(domain)
        print("[+] Resolved " + str(domain) + " -> " + str(ip_address))
        return ip_address
    except socket.gaierror:
        print("[!] Error: Unable to resolve IP for domain: " + str(domain))
        return None


def get_whois_info(domain):
    """Queries WHOIS database for domain registration details."""
    print("[*] Querying WHOIS records...")
    try:
        w = whois.whois(domain)
        whois_data = {
            "registrar": w.registrar,
            "creation_date": str(w.creation_date),
            "expiration_date": str(w.expiration_date),
            "name_servers": w.name_servers if isinstance(w.name_servers, list) else [w.name_servers],
            "emails": w.emails if isinstance(w.emails, list) else [w.emails],
            "org": w.org
        }
        return whois_data
    except Exception as e:
        print("[!] WHOIS query failed: " + str(e))
        return {"error": "WHOIS lookup failed"}


def get_shodan_info(ip_address, api_key):
    """Queries the Shodan API for open ports, banners, and vulnerabilities."""
    if not api_key:
        print("[!] Skipping Shodan lookup: SHODAN_API_KEY environment variable not set.")
        return {"notice": "Shodan API key missing"}

    print("[*] Querying Shodan for IP: " + str(ip_address) + "...")
    try:
        api = shodan.Shodan(api_key)
        host_info = api.host(ip_address)
        
        shodan_data = {
            "ip": host_info.get("ip_str"),
            "organization": host_info.get("org", "N/A"),
            "os": host_info.get("os", "N/A"),
            "open_ports": host_info.get("ports", []),
            "vulnerabilities": list(host_info.get("vulns", []))
        }
        return shodan_data
    except shodan.APIError as e:
        print("[!] Shodan API Error: " + str(e))
        return {"error": str(e)}


def save_report(domain, report_data, output_dir="reports"):
    """Saves gathered OSINT data as a formatted JSON report."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = domain + "_" + timestamp + ".json"
    filepath = os.path.join(output_dir, filename)

    try:
        with open(filepath, "w") as f:
            json.dump(report_data, f, indent=4)
        print("[+] Report saved successfully to: " + filepath)
        return filepath
    except IOError as e:
        print("[!] Failed to write report to file: " + str(e))
        return ""


def main():
    parser = argparse.ArgumentParser(description="OSINT Domain & Infrastructure Reconnaissance Script")
    parser.add_argument("-d", "--domain", required=True, help="Target domain (e.g., example.com)")
    args = parser.parse_args()

    domain = args.domain.strip().lower()

    # 1. Resolve Domain IP
    target_ip = get_domain_ip(domain)

    # 2. Collect WHOIS Data
    whois_info = get_whois_info(domain)

    # 3. Retrieve Shodan Infrastructure Data
    shodan_key = os.getenv("SHODAN_API_KEY")
    shodan_info = get_shodan_info(target_ip, shodan_key)

    # Compile Final Report
    full_report = {
        "target_domain": domain,
        "resolved_ip": target_ip,
        "scan_timestamp": str(datetime.now()),
        "whois_records": whois_info,
        "shodan_reconnaissance": shodan_info
    }

    # 4. Export Results
    save_report(domain, full_report)


if __name__ == "__main__":
    main()