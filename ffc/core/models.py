from django.db import models
from tinymce.models import HTMLField


class HomePage(models.Model):
    body = HTMLField(blank=True)
    is_published = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Home Page"

class SiteSettings(models.Model):
    business_name = models.CharField(max_length=120, default="FFC Cleaning")
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    service_area = models.CharField(max_length=200, blank=True)
    abn = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return "Site Settings"


class AboutPage(models.Model):
    hero_title = models.CharField(max_length=160, default="About FFC Cleaning")
    body = HTMLField(blank=True)
    team_blurb = HTMLField(blank=True)
    is_published = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "About Page"


class ServicesPage(models.Model):
    hero_title = models.CharField(max_length=160, default="Services")
    intro = HTMLField(blank=True)  # was TextField
    is_published = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Services Page"


class Service(models.Model):
    page = models.ForeignKey(ServicesPage, on_delete=models.CASCADE, related_name="services")
    name = models.CharField(max_length=120)
    description = HTMLField(blank=True)  # was TextField
    starting_from = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name


class ContactPage(models.Model):
    hero_title = models.CharField(max_length=160, default="Contact")
    intro = HTMLField(blank=True)  # was TextField
    show_contact_form = models.BooleanField(default=True)
    is_published = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Contact Page"


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    message = models.TextField()  # keep plain text (recommended)
    created_at = models.DateTimeField(auto_now_add=True)
    is_handled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.created_at:%Y-%m-%d})"


class QuoteRequest(models.Model):
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=40, blank=True)
    email = models.EmailField()
    suburb = models.CharField(max_length=120, blank=True)

    service_type = models.CharField(max_length=20, null=True, blank=True)
    bedrooms = models.PositiveSmallIntegerField(null=True, blank=True)
    bathrooms = models.PositiveSmallIntegerField(null=True, blank=True)

    preferred_date = models.DateField(null=True, blank=True)
    message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    is_contacted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.service_type or 'Quote'} ({self.created_at:%Y-%m-%d})"