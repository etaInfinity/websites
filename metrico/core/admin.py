from django.contrib import admin
from django.db import models

from tinymce.widgets import TinyMCE

from .models import (
    SiteSettings,
    )

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("business_name", "phone", "email")