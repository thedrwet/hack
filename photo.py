from PIL import Image
import exifread

def extract_photo_metadata(photo_path):
    # Open image file
    with open(photo_path, 'rb') as f:
        tags = exifread.process_file(f)

    # Extract metadata
    metadata = {}
    for tag in tags.keys():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
            metadata[tag] = str(tags[tag])

    return metadata

def main():
    photo_path = "D:\whatsapp\IMG20250307003214.jpg"
    metadata = extract_photo_metadata(photo_path)
    
    for key, value in metadata.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()