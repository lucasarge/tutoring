from functools import wraps
from django.shortcuts import redirect
from .models import Service

def survey_required(view):
    @wraps(view)
    def wrapped_view(request, *args, **kwargs):
    
        if "survey" not in request.path and "invite" not in request.path and "join" not in request.path:
            if not request.user.is_authenticated:
                return redirect('/users/login')
            
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
