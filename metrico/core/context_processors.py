from .models import Page

def core_nav_pages(request):
    pages = Page.objects.filter(is_published=True, show_in_nav=True).order_by("nav_order", "title")
    return {"nav_pages": pages}