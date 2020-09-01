import os
from caster_dashboard_2.settings.base import BASE_DIR


def get_current_version():
    # Read from VERSION file
    version_file = open(os.path.join(BASE_DIR, "VERSION"), "r")
    version = version_file.read()
    version_file.close()
    return version
