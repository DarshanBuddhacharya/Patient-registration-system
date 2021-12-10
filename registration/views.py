from django.core.checks.messages import Error
from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User, Group
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
    user = "none"
    error = ""
    if request.method == "POST":
        FirstName = request.POST['FirstName']
        LastName = request.POST['LastName']
        age = request.POST['age']
        gender = request.POST['gender']
        address = request.POST['address']
        PhoneNumber = request.POST['PhoneNumber']
        EmailAddress = request.POST['EmailAddress']
        Password = request.POST['Password']
        RepeatPassword = request.POST['RepeatPassword']
        BloodGroup = request.POST['BloodGroup']

        try:
            if Password == RepeatPassword:
                Patient.objects.create(FirstName=FirstName, LastName=LastName, age=age, gender=gender,
                                       address=address, PhoneNumber=PhoneNumber, EmailAddress=EmailAddress, BloodGroup=BloodGroup)
                user = User.objects.create_user(
                    FirstName=FirstName, LastName=LastName, EmailAddress=EmailAddress, username=EmailAddress)
                pat_group = Group.objects.get(name="Patient")
                pat_group.user_set.add(user)
                user.save()
                error = "no"
            else:
                error = "yes"
        except Exception as e:
            error = "no"
    d = {'error': error}
    return render(request, 'signup.html', d)
