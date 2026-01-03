from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "core/home.html")

def generators(request):
    return render(request, "core/core_generators.html")