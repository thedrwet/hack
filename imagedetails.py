from PIL import Image, ExifTags
import os
from datetime import datetime

def get_image_details(image_path):
    with Image.open(image_path) as img:
        file_stats = os.stat(image_path)
        details = {
            'Filename': img.filename,
            'Format': img.format,
            'Mode': img.mode,
            'Size (Pixels)': img.size,
            'Size (MB)': round(file_stats.st_size / (1024 * 1024), 2),
            'Created On': datetime.fromtimestamp(file_stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
        }

        exif_data = img._getexif()
        if exif_data is not None:
            for tag, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag, tag)
                details[tag_name] = value

        # Try to find the phone model information
        phone_model = details.get('Model', 'Unknown')
        details['Device'] = phone_model

    return details

if __name__ == '__main__':
    image_path = "D:\wallpaper\WhatsApp Image 2024-10-09 at 10.54.35_c4b561b5.jpg"  # Update this to your image file path
    details = get_image_details(image_path)
    for key, value in details.items():
        print(f"{key}: {value}")
