#!/usr/bin/env python3
"""
IP Recon Tool - IP geolocation & details lookup (OSINT)
Usage: python ip_recon.py 8.8.8.8
       python ip_recon.py            (interactive mode)
"""

import sys
import json
import requests

# Free APIs (no key needed). Key thakle rate limit beshi paye jaben.
APIS = [
    "http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,district,zip,lat,lon,timezone,isp,org,as,asname,mobile,proxy,hosting,query",
    "https://ipwho.is/{ip}",
    "https://ipinfo.io/{ip}/json",
]


def lookup_ip(ip: str):
    print(f"\n[*] Recon for: {ip}\n" + "=" * 50)
    for api in APIS:
        url = api.format(ip=ip)
        try:
            r = requests.get(url, timeout=10,
                             headers={"User-Agent": "Mozilla/5.0"})
            data = r.json()
        except Exception as e:
            print(f"[-] {url.split('/')[2]} failed: {e}")
            continue

        # ip-api er error format handle
        if data.get("status") == "fail" or data.get("success") is False:
            print(f"[-] {url.split('/')[2]}: {data.get('message')}")
            continue

        source = url.split("/")[2]
        print(f"\n[+] Source: {source}")
        print("-" * 50)

        # ipinfo er loc field (lat,lon) alada kore dekhai
        if "loc" in data:
            lat, lon = data["loc"].split(",")
            data["latitude"], data["longitude"] = lat, lon
            del data["loc"]

        for k, v in data.items():
            if k in ("readme",):  # ipinfo noise
                continue
            print(f"  {k:>15} : {v}")
        print()

        # Google Maps link
        lat = data.get("lat") or data.get("latitude")
        lon = data.get("lon") or data.get("longitude")
        if lat and lon:
            print(f"[+] Approx location (Google Maps): "
                  f"https://www.google.com/maps?q={lat},{lon}\n")
        break  # first successful API theke result pele enough


def main():
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = input("[?] IP address (blank = own IP): ").strip()

    # blank hole nijer public IP check hobe
    lookup_ip(target if target else "")


if __name__ == "__main__":
    main()