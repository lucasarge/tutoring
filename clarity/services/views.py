from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import login_required
from .models import Service, Invite, generate_code, Session, SubjectService, Resource, Document
from .forms import InviteForm, SessionForm, CaregiverForm, StudentForm, LinkForm, DocumentForm
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponseForbidden, JsonResponse, FileResponse, Http404
from .decorators import survey_required
from django.db.models import Q

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
    assign_form = None

    if page == "dashboard":

        if request.method == "POST":
            if "delete-link" in request.POST and next_session:
                next_session.link = ""
                next_session.save()
                return redirect(f"/services/{pk}/dashboard/")

            if "assign_resources" in request.POST:
                # assign_form = AssignDocumentForm(request.POST, instance=service)
                # if assign_form.is_valid():
                #     assign_form.save()
                    return redirect(f"/services/{pk}/dashboard/")
            
            else:
                link_form = LinkForm(request.POST, instance=next_session)
                if link_form.is_valid():
                    link_form.save()
                    return redirect(f"/services/{pk}/dashboard/")

        else:
            link_form = LinkForm()
            assign_form = None

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
    
    documents = None

    if page == "resources":
        documents = Resource.objects.filter(service=service)

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
        "session":next_session, 
        "documents":documents,
        "link_form":link_form,
        "assign_form":assign_form
    }

    return render(request, f"services/{page}.html", context)

@login_required
def all_services(request):
    if request.user.user_type != "tutor":
        raise HttpResponseForbidden()
    resources = Document.objects.all()
    services = Service.objects.all()
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/services/")
    else:
        form = DocumentForm()
    return render(request, "services/all-services.html", {"services": services,"resources": resources, "form": form})

def all_sessions(request):
    sessions = Session.objects.filter(
        Q(service__student=request.user)| 
        Q(service__caregiver=request.user)| 
        Q(service__tutor=request.user)
    ).distinct()

    session_list = []
    for session in sessions:
        session_list.append({
            'title': session.service.student.first_name.title(),
            'start': session.start.strftime("%Y-%m-%dT%H:%M:%S"),
            'end': session.end.strftime("%Y-%m-%dT%H:%M:%S") if session.end else None,
        })

    priv_sessions = Session.objects.filter(
        ~Q(service__student=request.user)| 
        ~Q(service__caregiver=request.user)| 
        ~Q(service__tutor=request.user)
    ).distinct()

    priv_session_list = []
    for priv_session in priv_sessions:
        priv_session_list.append({
            'title': priv_session.service.student.first_name.title(),
            'start': priv_session.start.strftime("%Y-%m-%dT%H:%M:%S"),
            'end': priv_session.end.strftime("%Y-%m-%dT%H:%M:%S") if priv_session.end else None,
        })

    return JsonResponse(session_list, safe=False)

def view_pdf(request, document_id):
    document = get_object_or_404(Document, id=document_id)

    try:
        pdf_file = open(document.file.path, 'rb')
        response = FileResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{document.title}.pdf"'
        return response
    except FileNotFoundError:
        raise Http404("PDF File not found.")