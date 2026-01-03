from django import template
from core.models import SiteSettings

register = template.Library()

@register.simple_tag
def site_settings():
    return SiteSettings.objects.get(pk=1)