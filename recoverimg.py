import pytsk3
import pyewf
import os

def recover_images_from_folder(image_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the disk image
    try:
        ewf_handle = pyewf.handle()
        ewf_handle.open(image_path)
    except IOError as e:
        print(f"Error opening EWF image: {e}")
        return

    try:
        volume = pytsk3.Img_Info(image_path)
        filesystem = pytsk3.FS_Info(volume)
    except Exception as e:
        print(f"Error accessing filesystem: {e}")
        return

    # Traverse the filesystem and find deleted images
    try:
        for directory in filesystem.open_dir(path='/'):
            for entry in directory:
                if entry.info.name.name == b'.' or entry.info.name.name == b'..':
                    continue
                if entry.info.meta and entry.info.meta.flags == pytsk3.TSK_FS_META_FLAG_UNALLOC:
                    try:
                        file_type = entry.info.meta.type
                        if file_type == pytsk3.TSK_FS_META_TYPE_REG:
                            # Check if the file is an image by extension
                            if entry.info.name.name.lower().endswith((b'.jpg', b'.jpeg', b'.png', b'.gif')):
                                file_name = entry.info.name.name.decode('utf-8')
                                print(f"Recovering {file_name}...")
                                output_path = os.path.join(output_folder, file_name)
                                file_data = entry.read_random(0, entry.info.meta.size)
                                with open(output_path, 'wb') as f:
                                    f.write(file_data)
                    except IOError as e:
                        print(f"Error reading file: {e}")
    except Exception as e:
        print(f"Error traversing filesystem: {e}")

if __name__ == '__main__':
    image_path = os.path.join("D:", "wallpaper", "drive2.E01") # Path to your disk image file
    output_folder = "recoveredimages"
    recover_images_from_folder(image_path, output_folder)
