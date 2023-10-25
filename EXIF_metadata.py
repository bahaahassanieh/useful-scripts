import json
from PIL import Image
import piexif


def extract_metadata(photo_location):
    with Image.open(photo_location) as img:
        # Check if the image has EXIF data
        if "exif" not in img.info:
            print("No EXIF metadata found in the image.")
            return {}

        # Extract exif data (metadata)
        exif_data = piexif.load(img.info['exif'])

        # Convert the data to a more JSON-friendly format
        metadata = {}
        for ifd_name in exif_data:
            if ifd_name != "thumbnail":
                for tag in exif_data[ifd_name]:
                    tag_name = piexif.TAGS[ifd_name][tag]["name"]
                    value = exif_data[ifd_name][tag]

                    # Convert bytes to string for JSON serialization
                    if isinstance(value, bytes):
                        value = value.decode(errors='replace')

                    metadata[tag_name] = value

        return metadata


if __name__ == "__main__":
    photo_location = input("Enter photo location: ")
    metadata = extract_metadata(photo_location)
    if metadata:
        print(json.dumps(metadata, indent=4))
