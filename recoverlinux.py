import recoverpy
import os
import shutil

def get_total_storage():
    total, used, free = shutil.disk_usage('/')
    return total

def get_file_system():
    statvfs = os.statvfs('/')
    return statvfs.f_fsid

def get_data_distribution():
    distribution = {}
    with open('uid.txt', 'w') as uid_file:
        for root, dirs, files in os.walk('/'):
            for file in files:
                path = os.path.join(root, file)
                try:
                    uid = os.stat(path).st_uid
                    distribution[path] = uid
                    uid_file.write(f"{uid}\n")
                except (FileNotFoundError, PermissionError):
                    # Skip files that are not found or cannot be accessed
                    continue
    return distribution

def recover_deleted_files():
    recoverpy.recover_files('/')

if __name__ == "__main__":
    print("Total Storage:", get_total_storage())
    print("File System:", get_file_system())
    print("Data Distribution:", get_data_distribution())
    recover_deleted_files()
    print("Deleted files have been recovered.")