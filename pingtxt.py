import subprocess
import re

def ping_host(hostname):
    process = subprocess.Popen(['ping', '-n', '4', hostname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')
    if process.returncode == 0:
        match = re.search(r'Packets: Sent = (\d+), Received = (\d+), Lost = (\d+)', stdout)
        if match:
            sent, received, lost = match.groups()
            loss_percentage = (int(lost) / int(sent)) * 100
            status = 'Success'
            return {'Status': status, 'Packets Sent': sent, 'Packets Received': received, 'Packet Loss (%)': f"{loss_percentage:.2f}"}
    return {'Status': 'Failure', 'Packets Sent': '0', 'Packets Received': '0', 'Packet Loss (%)': '100', 'Error': stderr}

def save_to_txt(data, filename='ping_results.txt'):
    with open(filename, 'w') as file:
        for entry in data:
            file.write(f"Hostname: {entry['Hostname']}\n")
            file.write(f"Status: {entry['Status']}\n")
            file.write(f"Packets Sent: {entry['Packets Sent']}\n")
            file.write(f"Packets Received: {entry['Packets Received']}\n")
            file.write(f"Packet Loss (%): {entry['Packet Loss (%)']}\n")
            file.write("\n")

def display_txt(filename='ping_results.txt'):
    with open(filename, 'r') as file:
        print(file.read())

if __name__ == '__main__':
    hosts = ['google.com','amazonprimegaming.com','fbabfbfajfbjaf.com']  # Hosts more likely to be accessible
    results = []
    for host in hosts:
        result = ping_host(host)
        result['Hostname'] = host
        results.append(result)

    save_to_txt(results)
    display_txt()
    print(f'Ping results saved to ping_results.txt')

