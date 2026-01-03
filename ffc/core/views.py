from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import Http404

from .models import SiteSettings, AboutPage, ServicesPage, ContactPage, HomePage
from .forms import ContactMessageForm, QuoteRequestForm


def _settings():
    return SiteSettings.objects.first()


def home(request):
    page = HomePage.objects.filter(is_published=True).first()
    return render(request, "core/home.html", {"page": page, "settings": _settings()})


def about(request):
    page = AboutPage.objects.filter(is_published=True).first()
    if not page:
        raise Http404("About page not set up yet.")
    return render(request, "core/about.html", {"page": page, "settings": _settings()})


def services(request):
    page = ServicesPage.objects.filter(is_published=True).first()
    if not page:
        raise Http404("Services page not set up yet.")

    services = page.services.filter(is_active=True)

    return render(
        request,
        "core/services.html",
        {
            "page": page,
            "services": services,
        },
    )


def contact(request):
    page = ContactPage.objects.filter(is_published=True).first()
    if not page:
        raise Http404("Contact page not set up yet.")

    form = ContactMessageForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("thanks_contact")

    return render(
        request,
        "core/contact.html",
        {"page": page, "form": form, "settings": _settings()},
    )


def quote(request):
    form = QuoteRequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("thanks_quote")
    return render(request, "core/quote.html", {"form": form, "settings": _settings()})


def thanks_contact(request):
    return render(request, "core/thanks_contact.html", {"settings": _settings()})


def thanks_quote(request):
    return render(request, "core/thanks_quote.html", {"settings": _settings()})