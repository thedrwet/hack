import subprocess
import os
def get_pendrive_path():
    for vol in os.popen('wmic logicaldisk get caption').read().splitlines():
        if 'Removable' in os.popen(f'wmic logicaldisk where "caption=\'{vol}\'" get description').read():
            return vol
    return None

pendrive_path = get_pendrive_path()

def recover_deleted_files(drive, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    # Replace 'testdisk' with the path to your recovery tool
    command = f'testdisk {drive} -o {output_folder}'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        print(f"Recovery complete! Files are in {output_folder}")

if __name__ == '__main__':
    drive = pendrive_path  # Update with your pendrive path
    output_folder = './recovered_files'
    recover_deleted_files(drive, output_folder)
