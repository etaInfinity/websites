from django.contrib import admin
from django.db import models

from tinymce.widgets import TinyMCE

from .models import Page

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_published", "show_in_nav", "nav_order")
    prepopulated_fields = {"slug": ("title",)}

    fieldsets = (
        ("Page Content", {
            "fields": ("title", "slug", "summary", "content", "template_name")
        }),
        ("Call To Action", {
            "fields": (
                "cta_enabled",
                "cta_heading",
                "cta_text",
                "cta_button_text",
                "cta_button_url",
            ),
        }),
        ("Visibility", {
            "fields": ("is_published", "show_in_nav", "nav_order")
        }),
    )