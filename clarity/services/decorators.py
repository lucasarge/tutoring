"""This is a decorators file that is used to restrict behaviour in a view."""

from functools import wraps
from django.shortcuts import redirect
from .models import Service
from django.http import HttpResponse

# Placed before a view used to make sure that the user accessing the page has filled out the survey required.
def survey_required(view):

    # Preserves functions original metadata helping for a range of things like debugging.
    @wraps(view)
    def wrapped_view(request, *args, **kwargs):

        # Makes exceptions for the invite and join page where survey won't be filled out yet.
        if "survey" not in request.path and "invite" not in request.path and "join" not in request.path:
            if not request.user.is_authenticated:
                return redirect('/users/login')

            # Checking to see if the survey field is empty or not. If it is empty redirect to survey page.
            if request.user.user_type == "caregiver":
                service = Service.objects.filter(caregiver=request.user).first()
                if service:
                    if not service.year or not service.caregiver_note:
                        return redirect(f'/services/{service.pk}/survey/')
                    
            elif request.user.user_type == "student":
                service = Service.objects.filter(student=request.user).first()
                if service:
                    if not service.student_note:
                        return redirect(f'/services/{service.pk}/survey/')

        return view(request, *args, **kwargs)
    return wrapped_view

def verified_tutor(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if request.user.user_type == "tutor" and request.user.profile.verified == False:
            return HttpResponse(
                "Error code: 403. Access denied. Verified tutor account required.", 
                content_type="text/plain", 
                status=403
            )
        return view_func(request, *args, **kwargs)
    return wrapped_view