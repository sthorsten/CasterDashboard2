from pathlib import Path
from uuid import uuid4
from django.conf import settings
from PIL import Image


def convert_square_logo(logo_path, logo_small_path, save_to):
    new_uuid = uuid4()

    orig_logo_path = Path(settings.MEDIA_ROOT, str(logo_path))
    orig_logo_small_path = Path(settings.MEDIA_ROOT, str(logo_small_path))

    if not orig_logo_path.is_file():
        return [None, None]

    path500 = Path(settings.MEDIA_ROOT, save_to,
                   f"{new_uuid}_500.webp").resolve()
    path50 = Path(settings.MEDIA_ROOT, save_to,
                  f"{new_uuid}_50.webp").resolve()

    with Image.open(orig_logo_path.resolve()) as image:
        image500 = image
        image500.resize([500, 500], Image.BICUBIC)
        image500.save(path500)

        image50 = image
        image50 = image50.resize([50, 50], Image.BICUBIC)
        image50.save(path50)

    if orig_logo_path.is_file():
        Path.unlink(orig_logo_path, True)
    if orig_logo_small_path.is_file():
        Path.unlink(orig_logo_small_path, True)

    return [f"{save_to}/{new_uuid}_500.webp", f"{save_to}/{new_uuid}_50.webp"]


def deleteLogoFiles(instance):
    orig_logo_path = Path(settings.MEDIA_ROOT, str(instance.logo))
    orig_logo_small_path = Path(settings.MEDIA_ROOT, str(instance.logoSmall))

    if orig_logo_path.is_file():
        Path.unlink(orig_logo_path, True)
    if orig_logo_small_path.is_file():
        Path.unlink(orig_logo_small_path, True)
