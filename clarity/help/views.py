"""This is a views file that holds functions or renders activated via url."""

from django.shortcuts import render
from .models import FAQ
from services.models import Service
from django.db.models import Q

# This is the help page view.
def help(request):

    # Collecting variables to display on the page.
    faq = FAQ.objects.all()
    if request.user.is_authenticated:
        service = Service.objects.filter(Q(student=request.user) | Q(caregiver=request.user)).first()
    else:
        service = None
    context = {"faq":faq, "service":service}

    # Rendering 'index.html' and parsing in context defined above.
    return render(request, 'help.html', context)