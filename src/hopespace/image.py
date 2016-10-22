from PIL import Image


EXIF_KEY = 274
ROTATIONS = {
   3: Image.ROTATE_180,
   6: Image.ROTATE_270,
   8: Image.ROTATE_90
}


def get_rotation(image):
    if not hasattr(image, '_getexif'):
        return None
    exif = image._getexif()
    if not exif or EXIF_KEY not in exif:
        return None
    orientation = exif[EXIF_KEY]

    if orientation not in ROTATIONS:
        return None
    return ROTATIONS[orientation]
