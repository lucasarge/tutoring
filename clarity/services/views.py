import zoneinfo

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import login_required
from clarity import settings
from .models import Service, Invite, generate_code, Session, SubjectService, Resource, Document
from .forms import InviteForm, SessionForm, CaregiverForm, StudentForm, LinkForm, DocumentForm, ShareResourceForm
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponseForbidden, JsonResponse, FileResponse, Http404
from .decorators import survey_required
from django.db.models import Q, Sum
from django.core.exceptions import PermissionDenied

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

            return redirect(f"/services/{service.pk}/survey", pk=service.pk)
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
@survey_required
def service(request, pk, page):

    service = Service.objects.get(pk=pk)

    if page == "admin" and request.user != service.tutor:
        raise HttpResponseForbidden()

    if request.user not in [
        service.student,
        service.caregiver,
        service.tutor
    ]:
        raise HttpResponseForbidden()
    
    form = None

    next_session = Session.objects.filter(
        service_id=pk,
        start__gt=timezone.now()
    ).order_by('start').first()


    link_form = None
    resource_form = None

    if page == "dashboard":

        if request.method == "POST":
            if "delete-link" in request.POST and next_session:
                next_session.link = ""
                next_session.save()
                return redirect(f"/services/{pk}/dashboard/")

            if "share_resources" in request.POST:
                share_resource_form = ShareResourceForm(request.POST)
                if share_resource_form.is_valid():
                    resource_form = share_resource_form.save(commit=False)
                    resource_form.tutor = request.user
                    resource_form.service = service
                    resource_form.save()
                    return redirect(f"/services/{pk}/dashboard/")
            
            else:
                link_form = LinkForm(request.POST, instance=next_session)
                if link_form.is_valid():
                    link_form.save()
                    return redirect(f"/services/{pk}/dashboard/")

        else:
            link_form = LinkForm()
            resource_form = ShareResourceForm()

    if page == "calendar":
        
        if request.method == "POST":
            form = SessionForm(request.POST, service=service)
            if form.is_valid():
                session = form.save(commit=False)
                session.service_id = pk
                session.cost = (session.duration*settings.GLOBAL_COST/60)
                session.end = session.start + timedelta(minutes=session.duration)
                session.save()
                return redirect(f"/services/{pk}/calendar/")
            else:
                print(form.errors)
        else:
            form = SessionForm(service=service)

    if page == "settings":
        if request.method == "POST":
            if request.user.user_type == "caregiver":
                form = CaregiverForm(request.POST, instance=service)
            elif request.user.user_type == "student":
                form = StudentForm(request.POST, instance=service)
            if form and form.is_valid():
                saved_service = form.save()

                if 'subject' in form.cleaned_data:
                    selected_subjects = form.cleaned_data['subject']

                    SubjectService.objects.filter(service=saved_service).exclude(subject__in=selected_subjects).delete()
                    
                    for subject in selected_subjects:
                        SubjectService.objects.get_or_create(service=saved_service, subject=subject)
                                
                return redirect(f"/services/{pk}/dashboard/")
    
    resources = Resource.objects.filter(service=service).order_by("-created")

    sessions = None
    total_cost = Session.objects.filter(completed=True, paid=False).aggregate(total=Sum('cost'))['total'] or 0
    total_fees = Session.objects.filter(cancelled=True, paid=False).aggregate(total=Sum('fees'))['total'] or 0
    total_owed = total_cost + total_fees
    unpaid = None

    if page == "payment":

        if request.method == "POST":
            if "cancel-session" in request.POST:
                session_id = request.POST.get("cancel-session")
                cancel_session = get_object_or_404(Session, id=session_id)

                if cancel_session.service.caregiver != request.user:
                    return redirect(f"/services/{pk}/{page}/")

                local_tz = zoneinfo.ZoneInfo("Pacific/Auckland")
                now = timezone.now().astimezone(local_tz)
                if now >= (cancel_session.start - timedelta(hours=1)):
                    return redirect(f"/services/{pk}/{page}/")

                if now.date() == cancel_session.start.date():
                    cancel_session.fees += 10
                else:
                    cancel_session.paid = True
                cancel_session.cancelled = True
                cancel_session.save()
                return redirect(f"/services/{pk}/{page}/")

        completed_status = request.GET.get('completed')
        paid_status = request.GET.get('paid')
        if completed_status == 'true':
            sessions = Session.objects.filter(completed=True)
        elif completed_status == 'false':
            sessions = Session.objects.filter(completed=False)
        elif paid_status == 'true':
            sessions = Session.objects.filter(paid=True)
        elif paid_status == 'false':
            sessions = Session.objects.filter(paid=False)
        else:
            current_time = timezone.now()
            upcoming = Session.objects.filter(start__gte=current_time).order_by("start")
            passed = Session.objects.filter(start__lt=current_time).order_by("-start")
            sessions = list(upcoming) + list(passed)
        unpaid = Session.objects.filter(Q(completed=True) | Q(cancelled=True), paid=False)        
        
    if page == "survey":
        if request.method == "POST":
            if request.user.user_type == "caregiver":
                form = CaregiverForm(request.POST, instance=service)
            elif request.user.user_type == "student":
                form = StudentForm(request.POST, instance=service)
            if form and form.is_valid():
                saved_service = form.save()

                if 'subject' in form.cleaned_data:
                    selected_subjects = form.cleaned_data['subject']

                    SubjectService.objects.filter(service=saved_service).exclude(subject__in=selected_subjects).delete()
                    
                    for subject in selected_subjects:
                        SubjectService.objects.get_or_create(service=saved_service, subject=subject)
                                
                return redirect(f"/services/{pk}/dashboard/")
        else:
            if request.user.user_type == "caregiver":
                form = CaregiverForm(instance=service)
            elif request.user.user_type == "student":
                form = StudentForm(instance=service)

    context = {
        "service":service, 
        "form":form, 
        "next_session":next_session, 
        "sessions":sessions,
        "resources":resources,
        "link_form":link_form,
        "resource_form":resource_form,
        "total_owed":total_owed,
        "unpaid": unpaid
    }
    
    return render(request, f"services/{page}.html", context)

@login_required
def all_services(request):
    if request.user.user_type != "tutor":
        raise HttpResponseForbidden()
    documents = Document.objects.all()
    services = Service.objects.all()
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/services/")
    else:
        form = DocumentForm()
    return render(request, "services/all-services.html", {"services": services,"documents": documents, "form": form})

def all_sessions(request):

    sessions = Session.objects.filter(end__gt=timezone.now(), cancelled=False)
    print(sessions)
    events = []

    for session in sessions:
        is_user = (session.service.student == request.user 
                   or session.service.caregiver == request.user 
                   or session.service.tutor == request.user)
        events.append({
            'title': f"{session.service.student.first_name.title()}: {session.subject}" if is_user else '',
            'start': timezone.localtime(session.start).strftime("%Y-%m-%dT%H:%M:%S"),
            'end': timezone.localtime(session.end).strftime("%Y-%m-%dT%H:%M:%S") if session.end else None,
            'display': 'auto' if is_user else 'background',
            'backgroundColor': '#808080' if not is_user else '',
            'extendedProps': {
                'isUser': is_user,
                'details': f"\nTutor: {session.service.tutor.first_name}\nSubject: {session.subject}\nNote: {session.note}" if is_user else ''
            }
        })

    return JsonResponse(events, safe=False)

def view_pdf(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)
    resource.opened = True
    resource.save()
    resource.refresh_from_db()
    document = resource.document

    try:
        pdf_file = open(document.file.path, 'rb')
        response = FileResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{document.title}.pdf"'
        return response
    except FileNotFoundError:
        raise Http404("PDF File not found.")

def view_session_link(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    is_authorised = Session.objects.filter(
        id=session_id
    ).filter(
        Q(service__caregiver=request.user) | 
        Q(service__student=request.user) | 
        Q(service__tutor=request.user)
    ).exists()

    if not is_authorised:
        raise PermissionDenied("You do not have permission to join this meeting. Contact me at 02040563805")

    session.completed = True
    session.save()

    return redirect(f"https://meet.google.com/{session.link}")


