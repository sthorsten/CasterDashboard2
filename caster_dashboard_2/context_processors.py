from caster_dashboard_2.version import get_current_version


def version_context(request):
    return {
        "version": get_current_version(),
        "theme": "dark",
    }
