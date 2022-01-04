
from django.shortcuts import render


def error_500(request, _exception=None):
    return render(request, "errors/error500.html", status=500)


def error_404(request, _exception=None):
    return render(request, "errors/error404.html", status=404)
