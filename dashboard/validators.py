from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_image(image):
    if not image:
        return

    try:
        image_file = image.file
    except FileNotFoundError:
        return

    # Validate file size
    current_file_size = image_file.size
    max_file_size = 500 * 1024  # 500kb
    if current_file_size > max_file_size:
        raise ValidationError(
            _('The file size exceeds the limit of 500 kB (is %(current_file_size)s kB)!'),
            params={'current_file_size': round(current_file_size / 1024, 2)}
        )

    # Validate file type
    if not image_file.name.lower().endswith('.png'):
        raise ValidationError(
            _('The image must be a .png file (is %(image_file_type)s)!'),
            params={'image_file_type': image_file.name.lower()}
        )

    # Validate image width & height
    if image.width > 500 or image.height > 500:
        raise ValidationError(
            _('The image must not be greater then 500x500 (is %(width)sx%(height)s)!'),
            params={'width': image.width, 'height': image.height}
        )


def validate_square_logo(image):
    if not image:
        return

    if image.height != image.width:
        raise ValidationError(
            _('Image must be square (is %(height)sx%(width)s)!'),
            params={'height': image.height, 'width': image.width}
        )
