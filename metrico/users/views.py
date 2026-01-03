from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.conf import settings

from .models import User


@login_required
def profile(request):
    # Private profile = current logged-in user
    return render(request, "users/profile.html", {"profile_user": request.user})


def public_profile(request, username: str):
    # Public profile view by username
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, "users/public_profile.html", {"profile_user": user})