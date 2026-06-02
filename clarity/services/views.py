from django.shortcuts import render, redirect
from django.contrib.auth.views import login_required
from .models import Service, Invite, generate_code, Session
from .forms import InviteForm, SessionForm
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponseForbidden, JsonResponse

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
            expires_at = timezone.now() + timedelta(minutes=10)
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
            invite.service = service
            invite.save()

            return redirect(f"/services/{service.pk}/dashboard", pk=service.pk)
    else:
        form = InviteForm()
        
    return render(request, "services/join.html", {"form":form})
            
def invite_status(request, pk):
    invite = Invite.objects.get(pk=pk)

    if invite.caregiver != request.user:
        return JsonResponse({}, status=403)
    
    expired = timezone.now() > invite.expires_at
    return JsonResponse({
        "used": invite.used,
        "expired": expired,
        "service_id": invite.service.id if invite.service else None
    })

@login_required
def service(request, pk, page):

    service = Service.objects.get(pk=pk)

    if request.user not in [
        service.student,
        service.caregiver
    ]:
        raise HttpResponseForbidden()
    
    form = None

    if page == "calendar":
        if request.method == "POST":
            form = SessionForm(request.POST)
            if form.is_valid():
                session = form.save(commit=False)
                session.service_id = pk
                session.end = session.start + timedelta(minutes=session.duration)
                session.save()
                return redirect(f"/services/{pk}/calendar/")
            else:
                print(form.errors)
        else:
            form = SessionForm()


    return render(request, f"services/{page}.html", {"service":service, "form":form})

def all_sessions(request):
    sessions = Session.objects.all()

    session_list = []
    for session in sessions:
        session_list.append({
            'title': session.service.student.first_name.title(),
            'start': session.start.strftime("%Y-%m-%dT%H:%M:%S"),
            'end': session.end.strftime("%Y-%m-%dT%H:%M:%S") if session.end else None,
        })
    return JsonResponse(session_list, safe=False)