import os
import psutil
from datetime import datetime, timedelta

def get_process_info():
    process_info = []
    for proc in psutil.process_iter(['pid', 'name', 'create_time']):
        try:
            pinfo = proc.info
            pinfo['create_time'] = datetime.fromtimestamp(pinfo['create_time'])
            process_info.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return process_info

def filter_yesterday_processes(process_info):
    yesterday = datetime.now() - timedelta(days=1)
    return [p for p in process_info if p['create_time'].date() == yesterday.date()]

def calculate_usage_time(process_info):
    usage_times = {}
    for p in process_info:
        pid = p['pid']
        try:
            proc = psutil.Process(pid)
            with proc.oneshot():
                if proc.status() == psutil.STATUS_RUNNING:
                    usage_time = datetime.now() - p['create_time']
                else:
                    usage_time = timedelta(seconds=0)
                usage_times[p['name']] = usage_times.get(p['name'], timedelta()) + usage_time
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return usage_times

def main():
    process_info = get_process_info()
    yesterday_processes = filter_yesterday_processes(process_info)
    usage_times = calculate_usage_time(yesterday_processes)
    
    with open(r'D:\hackathon\rt.txt', 'w') as file:
        for app, usage_time in usage_times.items():
            file.write(f"Application: {app}, Usage Time: {usage_time}\n")

if __name__ == "__main__":
    main()