from django.shortcuts import render, redirect
from .forms import RegisterServiceForm
from django.contrib.auth.views import login_required

# Create your views here.

@login_required
def connect(request):
    if request.method == "POST":
        form = RegisterServiceForm(request.POST, instance=request.user)
        if form.is_valid():
            service = form.save(commit=False)
            service.caregiver = request.user
            service.save()
            return redirect("/services/connect/")
    else:
        form = RegisterServiceForm(instance=request.user)
    return render(request, "services/connect.html", {"form": form})
