from django.shortcuts import render
# Create your views here.


def index(request):
    return render(request, 'index.html')


def contact(request):
    return render(request, 'contact.html')


def login(request):
    return render(request, 'login.html')


def help(request):
    return render(request, 'help.html')


def signup(request):
    return render(request, 'signup.html')
