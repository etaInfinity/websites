from django.urls import path
from . import views

app_name = "galaxy"

urlpatterns = [
    path("", views.index, name="index"),
    path("result/<int:seed>/", views.result, name="result"),
    path("map/<int:seed>.png", views.map_png, name="map_png"),
    path("system-map/<int:seed>/<int:system_index>.png", views.system_map_png, name="system_map_png"),
]