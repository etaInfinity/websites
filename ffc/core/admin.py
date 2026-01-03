from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (
    SiteSettings,
    AboutPage,
    ServicesPage,
    Service,
    ContactPage,
    ContactMessage,
    QuoteRequest,
    HomePage,
)

@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "body")

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("business_name", "phone", "email")

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "is_published", "updated_at")

class ServiceInline(admin.TabularInline):
    model = Service
    extra = 1

@admin.register(ServicesPage)
class ServicesPageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "is_published", "updated_at")
    inlines = [ServiceInline]

@admin.register(ContactPage)
class ContactPageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "is_published", "updated_at", "show_contact_form")

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created_at", "is_handled")
    list_filter = ("is_handled", "created_at")
    search_fields = ("name", "email", "phone", "message")
    ordering = ("-created_at",)

@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ("name", "service_type", "email", "phone", "created_at", "is_contacted")
    list_filter = ("service_type", "is_contacted", "created_at")
    search_fields = ("name", "email", "phone", "suburb", "message")
    ordering = ("-created_at",)