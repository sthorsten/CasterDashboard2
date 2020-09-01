import os
from PIL import Image
from caster_dashboard_2.settings.base import MEDIA_ROOT
from caster_dashboard_2.errors.ImageErrors import *


def convert_team_logo(team_id, current_image):
    path_500 = os.path.join(MEDIA_ROOT, "teams", str(team_id) + "_500.webp")
    path_50 = os.path.join(MEDIA_ROOT, "teams", str(team_id) + "_50.webp")

    convert_image(current_image, path_500, 500)
    convert_image(current_image, path_50, 50)


def convert_image(img, dst, size):
    image = Image.open(img)
    converted_image = image.resize((size, size))
    converted_image.save(dst)
