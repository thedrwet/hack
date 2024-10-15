import psutil
import time
from datetime import datetime
import csv
import os

def log_event(event):
    file_exists = os.path.isfile("event_log.csv")
    with open("event_log.csv", "a", newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "Event"])  # Write headers if the file doesn't exist
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), event])

def get_running_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'create_time']):
        try:
            process_info = proc.info
            process_info['create_time'] = datetime.fromtimestamp(process_info['create_time']).strftime("%Y-%m-%d %H:%M:%S")
            processes.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes

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

def main():
    log_event("Monitoring started")
    try:
        while True:
            processes = get_running_processes()
            for process in processes:
                log_event(f"Process: {process['name']} (PID: {process['pid']}) started at {process['create_time']}")
            log_cpu_usage()
            time.sleep(60)  # Log every 60 seconds
    except KeyboardInterrupt:
        log_event("Monitoring stopped")

if __name__ == "__main__":
    main()