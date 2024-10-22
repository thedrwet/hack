import pytsk3
import sys

def list_directories(image, parent, indent=0):
    for entry in parent:
        if entry.info.name.name in [b'.', b'..']:
            continue

        print(' ' * indent + entry.info.name.name.decode('utf-8'))

        if entry.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
            sub_directory = entry.as_directory()
            list_directories(image, sub_directory, indent + 4)

def extract_metadata(entry):
    print(f"Metadata for {entry.info.name.name.decode('utf-8')}:")
    print(f"Type: {entry.info.meta.type}")
    print(f"Size: {entry.info.meta.size}")
    print(f"UID: {entry.info.meta.uid}")
    print(f"GID: {entry.info.meta.gid}")
    print(f"Mode: {entry.info.meta.mode}")
    print(f"Creation Time: {entry.info.meta.crtime}")
    print(f"Modification Time: {entry.info.meta.mtime}")
    print(f"Access Time: {entry.info.meta.atime}")
    print(f"Change Time: {entry.info.meta.ctime}")

def main(image_path):
    img_info = pytsk3.Img_Info(image_path)
    fs_info = pytsk3.FS_Info(img_info)

    root_dir = fs_info.open_dir(path="/")
    list_directories(img_info, root_dir)

    for entry in root_dir:
        if entry.info.name.name not in [b'.', b'..']:
            extract_metadata(entry)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <image file>")
        sys.exit(1)

    image_path = sys.argv[1]
    main(image_path)