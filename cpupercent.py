import psutil
import time
from datetime import datetime
import csv
import os

def log_cpu_usage():
    file_exists = os.path.isfile("cpu_usage_log.csv")
    with open("cpu_usage_log.csv", "a", newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "PID", "Name", "Creation Time", "CPU Usage (%)"])  # Write headers if the file doesn't exist
        
        for proc in psutil.process_iter(['pid', 'name', 'create_time']):
            try:
                pinfo = proc.info
                pinfo['create_time'] = datetime.fromtimestamp(pinfo['create_time']).strftime("%Y-%m-%d %H:%M:%S")
                cpu_usage = proc.cpu_percent(interval=1.0)
                writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), pinfo['pid'], pinfo['name'], pinfo['create_time'], cpu_usage])
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

if __name__ == "__main__":
    log_cpu_usage()