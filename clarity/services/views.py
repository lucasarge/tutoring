from django.shortcuts import render, redirect
from .forms import RegisterServiceForm
from django.contrib.auth.views import login_required
from .models import Service

# Create your views here.

@login_required
def connect(request):
    if request.method == "POST":
        form = RegisterServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.caregiver = request.user
            service.save()
            return redirect("/services/connect/")
    else:
        form = RegisterServiceForm()
    return render(request, "services/connect.html", {"form": form})

@login_required
def service(request, slug):
    service = Service.objects.get(slug=slug)
    return render(request, 'services/service.html', {"service":service})