"""This is a views file that holds functions or renders activated via url."""

from django.shortcuts import render
from reviews.models import Review
from services.models import Subject, Service
from users.models import CustomUser
from django.db.models import Q, Avg

# This is the homepage view.
def index(request):

    # Collecting variables to display on the page.
    rating = Review.objects.aggregate(Avg('stars'))['stars__avg']
    subjects = Subject.objects.all()
    tutors = CustomUser.objects.filter(user_type='tutor')
    if request.user.is_authenticated:
        service = Service.objects.filter(Q(student=request.user) | Q(caregiver=request.user)).first()
    else:
        service = None
    context = {'subjects':subjects,'tutors':tutors,'service':service, 'rating':rating}
    
    # Rendering 'index.html' and parsing in context defined above.
    return render(request, 'index.html', context)