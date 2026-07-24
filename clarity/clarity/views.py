from django.shortcuts import render
from services.models import Subject
from users.models import CustomUser

def index(request):
    subjects = Subject.objects.all()
    tutors = CustomUser.objects.filter(user_type='tutor')
    return render(request, 'index.html', {'subjects':subjects,'tutors':tutors})