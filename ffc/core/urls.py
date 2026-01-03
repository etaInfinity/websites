from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("contact/", views.contact, name="contact"),
    path("quote/", views.quote, name="quote"),
    path("thanks/contact/", views.thanks_contact, name="thanks_contact"),
    path("thanks/quote/", views.thanks_quote, name="thanks_quote"),
]