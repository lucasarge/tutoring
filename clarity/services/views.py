"""This is a views file that holds functions or renders activated via url."""

import zoneinfo
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import login_required
from clarity import settings
from .models import Service, Invite, generate_code, Session, SubjectService, Resource, Document
from .forms import InviteForm, SessionForm, CaregiverForm, StudentForm, LinkForm, DocumentForm, ShareResourceForm
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponseForbidden, JsonResponse, FileResponse, Http404, HttpResponse
from .decorators import survey_required, verified_tutor
from django.db.models import Q, Sum

# Requires user to be logged in to access the invite page.
@login_required
def invite(request):

    # If user is not a caregiver redirect to forbidden page.
    if request.user.user_type != "caregiver":
        return HttpResponseForbidden()
    else:

        # Each time page is refreshed delete previous invite code.
        Invite.objects.filter(
            caregiver=request.user,
            used=False
        ).delete()

        # Create an invite from Invite model using generate_code from the models page.
        invite = Invite.objects.create(
            caregiver = request.user,
            code = generate_code(),
            expires_at = timezone.now() + timedelta(minutes=10)
        )

        # Rendering 'reviews.html' and parsing in invite defined above.
        if request.user.is_authenticated:
            service = Service.objects.filter(Q(student=request.user) | Q(caregiver=request.user)).first()
        else:
            service = None
        context = {"invite":invite, "service":service}
        return render(request, "services/invite.html", context)

# Requires user to be logged in to access the join page.
@login_required
def join(request):

    # If user is not a student redirect to forbidden page.
    if request.user.user_type != "student":
        return HttpResponseForbidden()

    # Checking if user is sending a response to the form.
    if request.method == "POST":
        form = InviteForm(request.POST)

        # If form is valid then proceed and collect code from form.  
        if form.is_valid():
            code = form.cleaned_data["code"]
            context = {"form":form}

            # Try check if there is an invite with the same code. If not send error.
            try:
                invite = Invite.objects.get(code=code)
            except Invite.DoesNotExist:
                form.add_error("code", "Invalid invite code")
                return render(request, "services/join.html", context)

            # Check if the invite code is over 10 minutes old if so then add expired error.
            if timezone.now() > invite.expires_at:
                form.add_error("code", "Invite expired")
                return render(request, "services/join.html", context)

            # Check if the invite code is already used if so send error message.
            if invite.used:
                form.add_error("code", "Invite already used")
                return render(request, "services/join.html", context)

            # Create new service with respective users as their respective roles.
            service = Service.objects.create(
                caregiver = invite.caregiver,
                student = request.user
            )

            # Sets invite to used and saves the update.
            invite.used = True
            invite.service = service
            invite.save()
            return redirect(f"/services/{service.pk}/survey", pk=service.pk)
    
    # If not sending response to the form then just display form.
    else:
        form = InviteForm()
        
    # Rendering 'join.html' and parsing in context defined above.
    if request.user.is_authenticated:
        service = Service.objects.filter(Q(student=request.user) | Q(caregiver=request.user)).first()
    else:
        service = None
    context = {"form":form, 'session':session}
    return render(request, "services/join.html", context)

# Polling request for invite_status to provide information to caregiver without them refreshing.
def invite_status(request, pk):
    invite = Invite.objects.get(pk=pk)
    expired = timezone.now() > invite.expires_at

    # Authenticates that the current user has access to the invites information.
    if invite.caregiver != request.user:
        return JsonResponse({}, status=403)

    # Return JsonResponse with all the relevant information about the status of the invite.
    return JsonResponse({
        "used": invite.used,
        "expired": expired,
        "service_id": invite.service.id if invite.service else None
    })

# Checks to see if user is authenticated and survey is completed.
@login_required
@survey_required
@verified_tutor
def service(request, pk, page):

    # Gets service through the primary key parsed in the url. 
    service = Service.objects.get(pk=pk)

    # Sets all these variables to none so they can be parsed through context.
    form = None
    link_form = None
    resource_form = None
    unpaid = None    
    sessions = None

    # Sets next_session to the session that is soonest.
    next_session = Session.objects.filter(
        service_id=pk,
        start__gt=timezone.now(),
        cancelled=False
    ).order_by('start').first()

    # Filter all resources to the services and in the order of the most recent first.
    resources = Resource.objects.filter(service=service).order_by("-created")

    # Calculate total_owed through all fees and costs.
    sessions = Session.objects.filter(Q(service__caregiver=request.user) | Q(service__student=request.user) | Q(service__tutor=request.user))
    total_cost = sessions.filter(completed=True, paid=False).aggregate(total=Sum('cost'))['total'] or 0
    total_fees = sessions.filter(cancelled=True, paid=False).aggregate(total=Sum('fees'))['total'] or 0
    total_owed = total_cost + total_fees

    # If current user is not apart of service then return forbidden page.
    if request.user not in [
        service.student,
        service.caregiver,
        service.tutor
    ]:
        raise HttpResponseForbidden()

    # If page is dashboard load the relevant information saving resources.
    if page == "dashboard":

        # Checking if user is sending a response to the form.
        if request.method == "POST":

            # Checking if form is delete-link and that next_session exists. 
            if "delete-link" in request.POST and next_session:
                next_session.link = ""
                next_session.save()
                return redirect(f"/services/{pk}/dashboard/")

            # Checking if form is share_resources by looking in the POST request.
            if "share_resources" in request.POST:
                share_resource_form = ShareResourceForm(request.POST)

                # If form is valid then set tutor and service and save.
                if share_resource_form.is_valid():
                    resource_form = share_resource_form.save(commit=False)
                    resource_form.tutor = request.user
                    resource_form.service = service
                    resource_form.save()
                    return redirect(f"/services/{pk}/dashboard/")

            if "cancel-session" in request.POST:
            
                # Getting cancel_session and time variables.
                session_id = request.POST.get("cancel-session")
                cancel_session = get_object_or_404(Session, id=session_id)
                local_tz = zoneinfo.ZoneInfo("Pacific/Auckland")
                now = timezone.now().astimezone(local_tz)

                # If user is not caregiver or student of service then prevent cancellation.
                if cancel_session.service.caregiver != request.user and cancel_session.service.student != request.user:
                    return redirect(f"/services/{pk}/{page}/")

                # Prevent cancellation if it starts within the next hour as a policy.
                if now >= (cancel_session.start - timedelta(hours=1)):
                    return redirect(f"/services/{pk}/{page}/")

                # Add $10 fee if the cancellation happens in the same day.
                if now.date() == cancel_session.start.date():
                    cancel_session.fees += 10

                # If cancellation happens a day prior don't add fee and set the session to paid.
                else:
                    cancel_session.paid = True

                # Set cancelled to true and save that then refresh.
                cancel_session.cancelled = True
                cancel_session.save()
                return redirect(f"/services/{pk}/{page}/")
            
            # Else the POST request must be for link_form and if form is valid save.
            else:
                link_form = LinkForm(request.POST, instance=next_session)
                if link_form.is_valid():
                    link_form.save()
                    return redirect(f"/services/{pk}/dashboard/")

        # If not a POST request get the forms to display them.
        else:
            link_form = LinkForm()
            resource_form = ShareResourceForm()

    # If page is calendar load the relevant information saving resources.
    if page == "calendar" and service.tutor:

        # Checking if user is sending a response to the form.        
        if request.method == "POST":
            form = SessionForm(request.POST, service=service)

            # If form is valid then set cost to GLOBAL_COST multipled by duration and other than details.
            if form.is_valid():
                session = form.save(commit=False)
                session.service_id = pk
                session.tutor = service.tutor
                session.cost = (session.duration*settings.GLOBAL_COST/60)
                session.end = session.start + timedelta(minutes=session.duration)
                session.save()
                return redirect(f"/services/{pk}/calendar/")

            # If form is not valid then print errors.
            else:
                print(form.errors)

        # If not a POST request get the form to display it.
        else:
            form = SessionForm(service=service)

    # If page is settings load the relevant information saving resources.
    if page == "settings":

        # Checking if user is sending a response to the form.
        if request.method == "POST":

            # Set form to respective form for user.
            if request.user.user_type == "caregiver":
                form = CaregiverForm(request.POST, instance=service)
            elif request.user.user_type == "student":
                form = StudentForm(request.POST, instance=service)

            # If form exists and is valid then update the form and create SubjectService objects for the Manytomany relationship.
            if form and form.is_valid():
                saved_service = form.save()
                if 'subject' in form.cleaned_data:
                    selected_subjects = form.cleaned_data['subject']
                    SubjectService.objects.filter(service=saved_service).exclude(subject__in=selected_subjects).delete()
                    for subject in selected_subjects:
                        SubjectService.objects.get_or_create(service=saved_service, subject=subject)          
                return redirect(f"/services/{pk}/dashboard/")

        # If not a POST request get the respective form to display it.
        else:
            if request.user.user_type == "caregiver":
                form = CaregiverForm(instance=service)
            elif request.user.user_type == "student":
                form = StudentForm(instance=service)

    # If page is payment load the relevant information saving resources.
    if page == "payment":

        # Removing access for student to access page.
        if request.user.user_type == "student":
                raise HttpResponseForbidden()
        
        # Checking if user is sending a response to the form.
        if request.method == "POST":
            if "cancel-session" in request.POST:

                # Getting cancel_session and time variables.
                session_id = request.POST.get("cancel-session")
                cancel_session = get_object_or_404(Session, id=session_id)
                local_tz = zoneinfo.ZoneInfo("Pacific/Auckland")
                now = timezone.now().astimezone(local_tz)

                # If user is not caregiver of service then prevent cancellation.
                if cancel_session.service.caregiver != request.user:
                    return redirect(f"/services/{pk}/{page}/")

                # Prevent cancellation if it starts within the next hour as a policy.
                if now >= (cancel_session.start - timedelta(hours=1)):
                    return redirect(f"/services/{pk}/{page}/")

                # Add $10 fee if the cancellation happens in the same day.
                if now.date() == cancel_session.start.date():
                    cancel_session.fees += 10

                # If cancellation happens a day prior don't add fee and set the session to paid.
                else:
                    cancel_session.paid = True

                # Set cancelled to true and save that then refresh.
                cancel_session.cancelled = True
                cancel_session.save()
                return redirect(f"/services/{pk}/{page}/")

        # Get boolean values from the path. Filter sessions to all that current user has access to.
        completed_status = request.GET.get('completed')
        paid_status = request.GET.get('paid')
        sessions = Session.objects.filter(Q(service__caregiver=request.user) | Q(service__student=request.user) | Q(service__tutor=request.user))
        unpaid = sessions.filter(Q(completed=True) | Q(cancelled=True), paid=False)
        
        # Filters sessions relative to boolean values requested.
        if completed_status == 'true':
            sessions = sessions.filter(completed=True)   
        elif completed_status == 'false':
            sessions = sessions.filter(completed=False)   
        elif paid_status == 'true':
            sessions = sessions.filter(paid=True)   
        elif paid_status == 'false':
            sessions = sessions.filter(paid=False)   

        # Else order all sessions in the soonest first and then the completed ones.
        else:
            current_time = timezone.now()
            upcoming = sessions.filter(start__gte=current_time).order_by("start")
            passed = sessions.filter(start__lt=current_time).order_by("-start")
            sessions = list(upcoming) + list(passed)     
        
    # If page is survey load the relevant information saving resources.
    if page == "survey":

        # Checking if user is sending a response to the form.
        if request.method == "POST":
            
            # Set form to respective form for user.
            if request.user.user_type == "caregiver":
                form = CaregiverForm(request.POST, instance=service)
            elif request.user.user_type == "student":
                form = StudentForm(request.POST, instance=service)

            # If form exists and is valid then update the form and create SubjectService objects for the Manytomany relationship.
            if form and form.is_valid():
                saved_service = form.save()
                if 'subject' in form.cleaned_data:
                    selected_subjects = form.cleaned_data['subject']
                    SubjectService.objects.filter(service=saved_service).exclude(subject__in=selected_subjects).delete()
                    for subject in selected_subjects:
                        SubjectService.objects.get_or_create(service=saved_service, subject=subject)
                return redirect(f"/services/{pk}/dashboard/")

        # If not a POST request get the respective form to display it.
        else:
            if request.user.user_type == "caregiver":
                form = CaregiverForm(instance=service)
            elif request.user.user_type == "student":
                form = StudentForm(instance=service)

    # Context for all of the pages that are specific to an individuals service page.
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

    # Rendering respective page and parsing in context defined above.
    return render(request, f"services/{page}.html", context)

# Requires user to be logged in to access the all_services page for tutors.
@login_required
@verified_tutor
def all_services(request):

    # Authenticates only tutors can access this page.
    if request.user.user_type != "tutor":
        raise HttpResponseForbidden()

    # Collect objects to display on the all_services page.
    documents = Document.objects.filter(creator=request.user)
    services = Service.objects.filter(tutor=request.user)
    total_cost = Session.objects.filter(paid=True, tutor=request.user).aggregate(total=Sum('cost'))['total'] or 0
    total_fees = Session.objects.filter(paid=True, tutor=request.user).aggregate(total=Sum('fees'))['total'] or 0
    owed_cost = Session.objects.filter(paid=False, tutor=request.user).aggregate(total=Sum('cost'))['total'] or 0
    owed_fees = Session.objects.filter(paid=False, tutor=request.user).aggregate(total=Sum('fees'))['total'] or 0
    profit = total_cost + total_fees
    owed = owed_cost + owed_fees

    # Checking if user is sending a response to the form and if is valid save and redirect.
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/services/")

    # If not sending response to the form then just display form.
    else:
        form = DocumentForm()

    # Rendering 'all-services.html' and parsing in context defined below.
    context = {"services": services, "resources": documents, "form": form, "profit":profit, "owed":owed}
    return render(request, "services/all-services.html", context)

# View used for displaying all the sessions on FullCalendar.
def all_sessions(request):

    # Get all sessions that haven't finished yet and that the current user is allowed to see.
    sessions = Session.objects.filter(
        end__gt=timezone.now(),
        cancelled=False,
    ).filter(
        Q(service__student=request.user)
        | Q(service__caregiver=request.user)
        | Q(service__tutor=request.user)
    )
    events = []

    # For each session note if user has access to session information and append relevant information to events for FullCalendar to handle.
    for session in sessions:
        is_user = (session.service.student == request.user 
                   or session.service.caregiver == request.user 
                   or session.service.tutor == request.user)
        events.append({

            # Hide session information if user does not have access to the session.
            'title': f"{session.service.student.first_name.title()}: {session.subject}" if is_user else '',
            'start': timezone.localtime(session.start).strftime("%Y-%m-%dT%H:%M:%S"),
            'end': timezone.localtime(session.end).strftime("%Y-%m-%dT%H:%M:%S") if session.end else None,
            'display': 'auto' if is_user else 'background',
            'backgroundColor': '#808080' if not is_user else '',
            'extendedProps': {
                'isUser': is_user,
                'details': f"\nTutor: {session.tutor.first_name}\nSubject: {session.subject}\nNote: {session.note}" if is_user else ''
            }
        })

    # Return JsonResponse with events included for FullCalendar to render.
    return JsonResponse(events, safe=False)

# View used to handle opening resource pdfs.
def view_pdf(request, resource_id):

    # Get resource through resource_id parsed through path then set opened to True.
    resource = get_object_or_404(Resource, id=resource_id)
    resource.opened = True
    resource.save()

    # Refresh resource and set document to the PDF inside resource.
    resource.refresh_from_db()
    document = resource.document

    # Try open the PDF and if file is not found return error.
    try:
        pdf_file = open(document.file.path, 'rb')
        response = FileResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{document.title}.pdf"'
        return response
    except FileNotFoundError:
        raise Http404("PDF File not found.")

# View used for student to be able to click on the link to session and open it in Google Meets.
def view_session_link(request, session_id):

    # Get session and authorise user has access to go to link.
    session = get_object_or_404(Session, id=session_id)
    is_authorised = Session.objects.filter(
        id=session_id
    ).filter(
        Q(service__caregiver=request.user) | 
        Q(service__student=request.user) | 
        Q(service__tutor=request.user)
    ).exists()

    # If not authorised provide error message with contact details.
    if not is_authorised:
        return HttpResponse(
            "You do not have permission to join this meeting. Contact me at 02040563805", 
            content_type="text/plain", 
            status=403
        )

    # If authorised set completed equal to True and save and redirect to link.
    session.completed = True
    session.save()
    return redirect(f"https://meet.google.com/{session.link}")
