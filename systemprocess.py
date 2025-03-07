import psutil

def list_all_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            process_info = proc.info
            processes.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes

if __name__ == "__main__":
    all_processes = list_all_processes()
    for process in all_processes:
        print(process)