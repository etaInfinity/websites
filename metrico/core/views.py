from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import Page


def home(request):
    # Home is just a Page with slug="home"
    page = get_object_or_404(Page, slug="home", is_published=True)
    return render(request, page.template_name, {"page": page})


def page_detail(request, slug: str):
    page = get_object_or_404(Page, slug=slug, is_published=True)
    return render(request, page.template_name, {"page": page})