import os
import hashlib
import csv
from datetime import datetime

def compute_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def list_files_and_hashes(root_dir):
    file_data = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            sha256 = compute_sha256(file_path)
            file_data.append([dirpath, filename, sha256])
    return file_data

def save_to_csv(file_data, output_file):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Directory", "File", "SHA-256"])
        writer.writerows(file_data)

if __name__ == "__main__":
    root_directory = "d:/hackkathon/hack/fileintegrity" # Change this to your target directory
    file_data = list_files_and_hashes(root_directory)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_csv = f"file_integrity_{timestamp}.csv"
    save_to_csv(file_data, output_csv)
    print(f"File integrity data saved to {output_csv}")