from django.core.exceptions import ValidationError
from PIL import Image

def validate_image_format(image):
    try:
        with Image.open(image) as img:
            img.verify()
            if img.format not in ('JPEG', 'JPG', 'PNG', 'GIF'):
                raise ValidationError('Unsuported image format.')
    except Exception:
        raise ValidationError('Invalid image file')