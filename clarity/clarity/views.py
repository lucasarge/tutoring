from django.shortcuts import render
from services.models import Subject, Service
from users.models import CustomUser
from django.db.models import Q

def index(request):
    subjects = Subject.objects.all()
    tutors = CustomUser.objects.filter(user_type='tutor')
    service = Service.objects.filter(Q(student=request.user) | Q(caregiver=request.user)).first()
    return render(request, 'index.html', {'subjects':subjects,'tutors':tutors,'service':service})