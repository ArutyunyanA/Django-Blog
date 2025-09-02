from django.core.exceptions import ValidationError
from PIL import Image

def validate_image_format(image):
    try:
        image.file.seek(0)
        img = Image.open(image.file)
        img.verify()
        if img.format not in ['JPEG', 'PNG']:
            raise ValidationError('Unsuported file format. Only JPEG, PNG and WEBP are allowed')
    except Exception:
        raise ValidationError('Invalid image file.')

