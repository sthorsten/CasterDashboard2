from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.translation import gettext_lazy as _


def validate_image(image):
    if not image:
        return

    if isinstance(image, InMemoryUploadedFile):
        return

    try:
        image_file = image.file
    except FileNotFoundError:
        return

    # Validate file size
    current_file_size = image_file.size
    max_file_size = 1024 * 1024  # 1MB
    if current_file_size > max_file_size:
        raise ValidationError(
            _('The file size exceeds the limit of 1 MB (is %(current_file_size)s MB)!'),
            params={'current_file_size': round(current_file_size / (1024 * 1024), 2)}
        )


def validate_square_logo(image):
    if not image:
        return

    if isinstance(image, InMemoryUploadedFile):
        return

    try:
        image_file = image.file
    except FileNotFoundError:
        return

    if image.height != image.width:
        raise ValidationError(
            _('Image must be square (is %(height)sx%(width)s)!'),
            params={'height': image.height, 'width': image.width}
        )
