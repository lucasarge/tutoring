"""This is a views file that holds functions or renders activated via url."""

from django.shortcuts import render
from .models import FAQ

# This is the help page view.
def help(request):

    # Collecting variables to display on the page.
    faq = FAQ.objects.all()
    context = {"faq":faq}

    # Rendering 'index.html' and parsing in context defined above.
    return render(request, 'help.html', context)