# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 19:40:09 2024

@author: thedr
"""

import subprocess
import csv
import re

def ping_host(hostname):
    # Execute the ping command
    process = subprocess.Popen(['ping', '-c', '4', hostname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # Decode the output and search for packet loss information
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')
    if process.returncode == 0:
        match = re.search(r'(\d+)\s+packets transmitted,\s+(\d+)\s+received,\s+(\d+)%\s+packet loss', stdout)
        if match:
            transmitted, received, loss = match.groups()
            status = 'Success' if int(loss) == 0 else 'Failure'
            return {'Status': status, 'Packets Sent': transmitted, 'Packets Received': received, 'Packet Loss (%)': loss}
    return {'Status': 'Failure', 'Error': stderr}

def save_to_csv(data, filename='ping_results.csv'):
    # Define the headers
    headers = ['Hostname', 'Status', 'Packets Sent', 'Packets Received', 'Packet Loss (%)']

    # Write data to CSV
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

if __name__ == '__main__':
    hosts = ['example.com', 'google.com']  # Add more hosts as needed
    results = []
    for host in hosts:
        result = ping_host(host)
        result['Hostname'] = host
        results.append(result)

    save_to_csv(results)
    print('Ping results saved to ping_results.csv')
