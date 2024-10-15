import os
import re
import socket
import subprocess

def get_ip_addresses():
    ip_addresses = set()
    with os.popen('netstat -n') as netstat_output:
        for line in netstat_output:
            match = re.search(r'\d+\.\d+\.\d+\.\d+', line)
            if match:
                ip_addresses.add(match.group())
    return ip_addresses

def get_mac_addresses():
    mac_addresses = set()
    with os.popen('getmac') as getmac_output:
        for line in getmac_output:
            match = re.search(r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', line)
            if match:
                mac_addresses.add(match.group())
    return mac_addresses

def get_dns_info():
    dns_info = []
    with os.popen('ipconfig /all') as ipconfig_output:
        for line in ipconfig_output:
            if 'DNS Servers' in line:
                dns_info.append(line.strip())
    return dns_info

def main():
    ip_addresses = get_ip_addresses()
    mac_addresses = get_mac_addresses()
    dns_info = get_dns_info()

    with open('network_info.txt', 'w') as file:
        file.write("IP Addresses Visited:\n")
        for ip in ip_addresses:
            file.write(f"{ip}\n")
        
        file.write("\nMAC Addresses:\n")
        for mac in mac_addresses:
            file.write(f"{mac}\n")
        
        file.write("\nDNS Server Information:\n")
        for dns in dns_info:
            file.write(f"{dns}\n")

if __name__ == "__main__":
    main()