from django.db import models
from django.utils.text import slugify


class SiteSettings(models.Model):
    business_name = models.CharField(max_length=120, default="Metrico")
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    service_area = models.CharField(max_length=200, blank=True)
    abn = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return "Site Settings"