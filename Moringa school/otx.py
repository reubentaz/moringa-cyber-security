import requests

def fetch_threat_intelligence(indicator):
    # API setup for AlienVault OTX
    url = f"https://otx.alienvault.com/api/v1/indicators/IPv4/{indicator}/general"
    headers = {"X-OTX-API-KEY": "YOUR_ACTUAL_API_KEY"} 
    
    response = requests.get(url, headers=headers)
    return response.json()

def parse_threat_intelligence(data):
    # 1. Validation
    if not data or 'pulse_info' not in data or 'pulses' not in data['pulse_info']:
        print("\nSECUREHEALTH PRIORITIZED THREAT REPORT\nTotal Pulses Found: 0")
        return

    pulses = data['pulse_info']['pulses']
    high_priority_keywords = ["ransomware", "phishing", "malware", "cobalt strike"]

    # 2. File Export Logic
    with open("otx_intelligence_report.txt", "w") as report_file:
        header = f"{'='*60}\nSECUREHEALTH PRIORITIZED THREAT REPORT\n{'='*60}\n"
        print(header)
        report_file.write(header)

        for i, pulse in enumerate(pulses):
            name = pulse.get('name', 'Unknown Threat')
            tags = pulse.get('tags', [])
            
            # 3. Analysis: Priority Flagging
            is_high = any(k.lower() in [t.lower() for t in tags] for k in high_priority_keywords)
            priority = "HIGH" if is_high else "LOW"

            output = (
                f"\n[Pulse #{i+1}] {name}\n"
                f"PRIORITY: {priority}\n"
                f"Tags:     {', '.join(tags) if tags else 'None'}\n"
                f"Indicators:\n"
            )
            
            indicators = pulse.get('indicators', [])
            for ioc in indicators[:3]:
                output += f"  -> {ioc.get('type')}: {ioc.get('indicator')}\n"
            
            output += "-" * 30 + "\n"
            print(output)
            report_file.write(output)

        footer = f"{'='*60}\nEND OF REPORT\n"
        print(footer)
        report_file.write(footer)

if __name__ == "__main__":
    # Final test indicator
    test_indicator = "118.107.177.106" 
    raw_data = fetch_threat_intelligence(test_indicator)
    parse_threat_intelligence(raw_data)