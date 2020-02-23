from django.shortcuts import render

def home(request):
    return render(request, 'github/home.html')

def info(request):
    return render(request, 'github/info.html')


