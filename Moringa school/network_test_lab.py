#!/usr/bin/env python3
"""
network_test_lab.py
A network auditing tool for Junior Security Analysts to verify interface status,
connectivity, DNS resolution, and listening services.
"""

import os
import sys
import socket
import subprocess


def check_permissions():
    """
    Ensures the script is running with administrative (root) privileges.
    Exits with code 1 and a usage message if check fails.
    """
    if os.geteuid() != 0:
        print("ERROR: Administrative privileges required.")
        print("USAGE: sudo python3 network_test_lab.py")
        sys.exit(1)
    print("[+] Administrative permissions verified.")


def get_local_ips():
    """
    Displays IPv4 and IPv6 addresses for all active network interfaces.
    """
    print("\n--- [1] Network Interface Audit ---")
    try:
        # Utilizing 'ip addr' for a comprehensive view of all families
        output = subprocess.check_output(["ip", "addr", "show"], text=True)
        print(output)
    except FileNotFoundError:
        print("[-] Error: 'ip' command not found. Ensure you are on a Linux system.")


def ping_test():
    """
    Tests connectivity to Google's public DNS server (8.8.8.8).
    """
    target = "8.8.8.8"
    print(f"\n--- [2] Connectivity Test: {target} ---")
    # -c 2 sends two packets, -W 2 sets a 2-second timeout
    result = subprocess.run(
        ["ping", "-c", "2", "-W", "2", target],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(f"[+] Connectivity to {target} is successful.")
    else:
        print(f"[-] Connectivity to {target} failed.")


def dns_ping_test():
    """
    Tests DNS resolution and connectivity using flatironschool.com.
    """
    domain = "flatironschool.com"
    print(f"\n--- [3] DNS Resolution Test: {domain} ---")
    try:
        ip_addr = socket.gethostbyname(domain)
        print(f"[+] DNS Success: {domain} resolved to {ip_addr}")
        
        # Verify connectivity to the resolved IP
        ping_res = subprocess.run(
            ["ping", "-c", "1", "-W", "2", ip_addr],
            capture_output=True
        )
        if ping_res.returncode == 0:
            print(f"[+] ICMP reachability to {domain} ({ip_addr}) verified.")
    except socket.gaierror:
        print(f"[-] DNS Error: Could not resolve {domain}.")


def check_local_listeners():
    """
    Identifies processes listening on open ports using 'ss'.
    Equivalent to netstat but more modern and accurate.
    """
    print("\n--- [4] Local Listeners & Open Ports ---")
    try:
        # -l: listening, -n: numeric, -t: tcp, -u: udp, -p: process info
        output = subprocess.check_output(["ss", "-lntup"], text=True)
        print(output)
    except Exception as e:
        print(f"[-] Failed to audit ports: {e}")


def main():
    """
    Orchestrates the network audit functions.
    """
    print("==============================================")
    print("       NETWORK TEST LAB: SECURITY AUDIT       ")
    print("==============================================")
    
    # Permission check must occur first
    check_permissions()
    
    # Run audit functions
    get_local_ips()
    ping_test()
    dns_ping_test()
    check_local_listeners()
    
    print("\n==============================================")
    print("              AUDIT CONCLUDED                 ")
    print("==============================================")


if __name__ == "__main__":
    main()