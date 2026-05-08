from django.shortcuts import render, redirect
from django.contrib.auth.views import login_required
from .models import Service, Invite, generate_code
from .forms import InviteForm
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponseForbidden

# Create your views here.

@login_required
def invite(request):

    if request.user.user_type != "caregiver":
        return HttpResponseForbidden()
    
    else:
        Invite.objects.filter(
            caregiver=request.user,
            used=False
        ).delete()

        invite = Invite.objects.create(
            caregiver = request.user,
            code = generate_code(),
            expires_at = timezone.now() + timedelta(minutes=30)
        )

        return render(request, "services/invite.html", {"invite":invite})

@login_required
def join(request):
    
    if request.user.user_type != "student":
        return HttpResponseForbidden()
    
    if request.method == "POST":
        form = InviteForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]

            try:
                invite = Invite.objects.get(code=code)
            except Invite.DoesNotExist:
                form.add_error("code", "Invalid invite code")
                return render(request, "services/join.html", {"form":form})
            
            if timezone.now() > invite.expires_at:
                form.add_error("code", "Invite expired")
                return render(request, "services/join.html", {"form":form})
            
            if invite.used:
                form.add_error("code", "Invite already used")
                return render(request, "services/join.html", {"form":form})
            
            service = Service.objects.create(
                caregiver = invite.caregiver,
                student = request.user
            )

            invite.used = True
            invite.save()

            return redirect("/users/profile", pk=service.pk)
    else:
        form = InviteForm()
        
    return render(request, "services/join.html", {"form":form})
            
@login_required
def service(request, pk):

    service = Service.objects.get(pk=pk)

    if request.user not in [
        service.student,
        service.caregiver
    ]:
        raise HttpResponseForbidden()

    return render(request, "services/service.html", {"service":service})


