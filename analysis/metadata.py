
import os
from PIL import Image


class ImageMetadataAnalyzer:

    def analyze(self, image_path):

        if not os.path.exists(image_path):
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        image = Image.open(image_path)

        exif_data = image.getexif()

        camera_make = None
        camera_model = None
        software = None

        if exif_data:

            camera_make = exif_data.get(271)
            camera_model = exif_data.get(272)
            software = exif_data.get(305)

        return {

            "filename": os.path.basename(image_path),

            "file_size_bytes":
                os.path.getsize(image_path),

            "format":
                image.format,

            "width":
                image.width,

            "height":
                image.height,

            "color_mode":
                image.mode,

            "has_exif":
                bool(exif_data),

            "camera_make":
                camera_make,

            "camera_model":
                camera_model,

            "software":
                software
        }
