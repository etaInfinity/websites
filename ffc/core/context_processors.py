from .models import SiteSettings

def site_settings(request):
    """
    Makes SiteSettings available in all templates as `site_settings`
    """
    return {
        "site_settings": SiteSettings.objects.first()
    }