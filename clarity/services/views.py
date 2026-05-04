from django.shortcuts import render, redirect
from .forms import RegisterServiceForm
from django.contrib.auth.views import login_required

# Create your views here.

@login_required
def connect(request):
    if request.method == "POST":
        form = RegisterServiceForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("/services/connect/")
