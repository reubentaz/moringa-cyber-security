"""
Passive Scanning Script for OT Environment (Medical Device Manufacturing)
- Captures network packets passively
- Filters OT protocols (Modbus, DNP3, BACnet)
- Logs relevant data for analysis
- Does NOT send packets or alter traffic
"""

import pyshark

# Function to start network capture (To be completed in later steps)
def capture_packets(interface):
    """
    Capture packets passively and handle errors.
    """
    try:
        print(f"Listening on {interface}...")
        capture = pyshark.LiveCapture(interface=interface)
        for packet in capture.sniff_continuously(packet_count=50):
            try:
                filter_ot_traffic(packet)
            except Exception as e:
                print(f"Error processing packet: {e}")
    except Exception as e:
        print(f"Error capturing packets: {e}")
# Function to filter OT protocols (To be completed in later steps)
def filter_ot_traffic(packet):
    """
    Filters packets to identify OT-related traffic.
    """
    try:
        if 'MODBUS' in packet or 'DNP3' in packet or 'BACnet' in packet:
            src_ip = packet.ip.src
            dest_ip = packet.ip.dst
            protocol = packet.highest_layer
            log_data(f"OT Traffic Detected: {protocol} from {src_ip} to {dest_ip}")
    except AttributeError:
        pass  # Ignore packets without IP or protocol layers

# Function to log captured data (To be completed in later steps)
def log_data(data):
    """
    Logs OT-related network traffic to a file.
    """
    with open("ot_scan_log.txt", "a") as log_file:
        log_file.write(data + "\n")
    print(data)  # Print to console for immediate visibility

# Main function (To be completed in later steps)
def main():
    interface = "eth0"  # Change this based on your network adapter
    print(f"Starting passive scanning on {interface}...")
    capture_packets(interface)

if __name__ == "__main__":
    print("Passive Scanning Script for OT Environment")
    print("Ensure you have the correct network interface configured.")
    print("Logs will be stored in ot_scan_log.txt")
    main()