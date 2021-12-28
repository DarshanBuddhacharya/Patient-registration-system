from django.core.checks import messages
from django.core.checks.messages import Error
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, authenticate
from django.contrib import messages
# Create your views here.


def index(request):
    return render(request, 'index.html')


def contact(request):
    return render(request, 'contact.html')


def doctors(request):

    docs = Doctor.objects.all()

    return render(request, 'doctors.html', {'docs': docs})


def loginPage(request):
    if request.method == "POST":
        u = request.POST['EmailAddress']
        p = request.POST['Password']

        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            g = request.user.groups.all()[0].name
            if g == 'Patient':
                return render(request, 'index.html')
        else:
            messages.success(
                request, ("Invalid username or password. Please try again.."))
            return redirect('login')
    else:
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
                    first_name=FirstName, email=EmailAddress, password=Password, username=EmailAddress)
                pat_group = Group.objects.get(name="Patient")
                pat_group.user_set.add(user)
                user.save()
                error = "no"
            else:
                messages.success(
                    request, ("Passwords do not match. Please try again"))
        except Exception as e:
            error = "yes"
    d = {'error': error}
    return render(request, 'signup.html', d)
