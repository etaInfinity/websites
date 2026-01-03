from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import (
    SiteSettings,
    )

def home(request):
    # Home is just a Page with slug="home"
    page = get_object_or_404(SiteSettings)
    return render(request, "core/home.html", {"page": page, "site_settings": SiteSettings})