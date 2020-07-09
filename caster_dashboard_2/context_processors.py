from dashboard.models import Version


def test_context(request):
    return {
        "version": Version.objects.filter().order_by('-id')[0],
        "theme": "dark",
    }
