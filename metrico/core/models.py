from django.db import models
from django.utils.text import slugify


class Page(models.Model):
    TEMPLATE_CHOICES = [
        ("core/page.html", "Standard Page"),
        ("core/home.html", "Home Page"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, help_text="Used in the URL, e.g. 'about', 'faq'")
    summary = models.CharField(max_length=300, blank=True)
    content = models.TextField(blank=True, help_text="HTML allowed (or plain text if you prefer).")
    template_name = models.CharField(max_length=100, choices=TEMPLATE_CHOICES, default="core/page.html")

    is_published = models.BooleanField(default=True)
    show_in_nav = models.BooleanField(default=True)
    nav_order = models.PositiveIntegerField(default=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    cta_enabled = models.BooleanField(default=False)
    cta_heading = models.CharField(max_length=200, blank=True)
    cta_text = models.CharField(max_length=300, blank=True)
    cta_button_text = models.CharField(max_length=100, blank=True)
    cta_button_url = models.CharField(max_length=300, blank=True)

    # existing meta / methods...

    class Meta:
        ordering = ["nav_order", "title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)