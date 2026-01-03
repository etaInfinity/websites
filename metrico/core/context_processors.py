# from .models import SiteSettings

# def site_settings(request):
#     return {
#         "site_settings": SiteSettings.objects.all()
#     }

from .models import SiteSettings

def site_settings(request):
    obj, _ = SiteSettings.objects.get_or_create(pk=1, defaults={"business_name": "Metrico"})
    return {"site_settings": obj}
