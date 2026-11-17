from urllib.parse import unquote
import sys
import requests

# Default target base URL (can be overridden via command line or modified)
BASE_URL = "http://localhost:5000/search?q="

# Allow AutoTest to pass target URL as a CLI argument if needed
if len(sys.argv) > 1:
    BASE_URL = sys.argv[1]

# Payloads to test for reflected input
payloads = [
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(2)>",
    "%3Csvg%2Fonload%3Dalert(3)%3E",
]


def test_payload(payload: str) -> bool:
    """Submit payload to target URL and check if reflected in response.

    Checks for both verbatim matches and URL-decoded matches.
    """
    try:
        full_url = BASE_URL + payload
        response = requests.get(full_url, timeout=5)

        # Decode payload in case an encoded variant was sent
        decoded_payload = unquote(payload)

        # Check if either raw or decoded payload appears in response text
        if payload in response.text or decoded_payload in response.text:
            print("[!] VULNERABLE: Payload reflected in response!")
            print(f"    Payload: {payload}")
            print(f"    Status Code: {response.status_code}\n")
            return True

        print("[-] SECURE: Payload was not reflected or was properly encoded.")
        print(f"    Payload: {payload}")
        print(f"    Status Code: {response.status_code}\n")
        return False

    except requests.exceptions.ConnectionError as e:
        print(f"[!] Connection failed for payload: {payload}")
        print(f"    Error: {e}\n")
        return False
    except requests.exceptions.Timeout as e:
        print(f"[!] Request timed out for payload: {payload}")
        print(f"    Error: {e}\n")
        return False
    except requests.exceptions.RequestException as e:
        print(f"[!] Request failed for payload: {payload}")
        print(f"    Error: {e}\n")
        return False


def main() -> None:
    """Execute main web vulnerability scanning workflow."""
    print("\n[+] Starting web vulnerability scan...\n")

    reflected_count = 0
    total_payloads = len(payloads)

    for payload in payloads:
        if test_payload(payload):
            reflected_count += 1

    print("========================================")
    print("           SCAN SUMMARY")
    print("========================================")
    print(f"Total Payloads Tested : {total_payloads}")
    print(f"Reflected (Vulnerable): {reflected_count}")
    print(f"Blocked/Clean (Secure): {total_payloads - reflected_count}")
    print("========================================\n")


if __name__ == "__main__":
    main()