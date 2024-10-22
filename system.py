import platform
import psutil
import shutil
import GPUtil

def get_system_info():
    # Get OS information
    os_info = platform.system()
    os_version = platform.version()

    # Get disk space information
    total, used, free = shutil.disk_usage("/")

    # Get RAM information
    ram_info = psutil.virtual_memory()
    total_ram = ram_info.total

    # Get GPU information
    gpus = GPUtil.getGPUs()
    gpu_info = gpus[0].name if gpus else "No GPU found"

    # Print system information
    print(f"Operating System: {os_info}")
    print(f"OS Version: {os_version}")
    print(f"Total Disk Space: {total // (2**30)} GB")
    print(f"Used Disk Space: {used // (2**30)} GB")
    print(f"Free Disk Space: {free // (2**30)} GB")
    print(f"Total RAM: {total_ram // (2**30)} GB")
    print(f"GPU: {gpu_info}")

if __name__ == "__main__":
    get_system_info()