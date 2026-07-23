from django.shortcuts import render
from .models import FAQ

# Create your views here.

def help(request):
    faq = FAQ.objects.all()
    return render(request, 'help.html', {"faq":faq})