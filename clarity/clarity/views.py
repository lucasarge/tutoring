from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def help(request):
    return render(request, 'help.html')