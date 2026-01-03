from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tinymce/", include("tinymce.urls")),
    path("accounts/", include("users.urls")),  # 👈 PREFIX
    path("", include("core.urls")),
]