import os
from PIL import Image, ImageOps
from caster_dashboard_2.settings import MEDIA_ROOT
from caster_dashboard_2.errors.ImageErrors import *


def convert_team_logo(team_id, current_image):
    path_500 = os.path.join(MEDIA_ROOT, "teams", str(team_id) + "_500.webp")
    path_50 = os.path.join(MEDIA_ROOT, "teams", str(team_id) + "_50.webp")

    convert_square_image(current_image, path_500, 500)
    convert_square_image(current_image, path_50, 50)


def convert_league_logo(league_id, current_image):
    path_500 = os.path.join(MEDIA_ROOT, "leagues", str(league_id) + "_500.webp")
    path_50 = os.path.join(MEDIA_ROOT, "leagues", str(league_id) + "_50.webp")

    convert_square_image(current_image, path_500, 500)
    convert_square_image(current_image, path_50, 50)


def convert_sponsor_logo(sponsor_id, current_image):
    path_100 = os.path.join(MEDIA_ROOT, "sponsors", str(sponsor_id) + "_100.webp")

    convert_non_square_image(current_image, path_100, 100)


def convert_square_image(img, dst, size):
    image = Image.open(img)
    converted_image = image.resize((size, size))
    converted_image.save(dst)


def convert_non_square_image(img, dst, target_height):
    image = Image.open(img)
    target_scaling = (target_height / image.height)
    converted_image = ImageOps.scale(image, target_scaling)
    converted_image.save(dst)
