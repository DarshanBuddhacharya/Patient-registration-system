import email
from sqlite3 import Time
from time import timezone
from django import template
from django.contrib import auth
from django.core.checks import messages
from django.core.checks.messages import Error
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


def index(request):
    return render(request, 'index.html')


def contact(request):
    return render(request, 'contact.html')


def booking(request):
    if not request.user.is_active:
        messages.success(
            request, ("In order to book an appointment you must login first"))
        return redirect('login')
    doctor_details = Doctor.objects.all()
    g = request.user.groups.all()[0].name
    if g == 'Patient':
        patient_details = Patient.objects.all().filter(EmailAddress=request.user)
        d = {'patient_details': patient_details,
             'doctor_details': doctor_details}

    if request.method == "POST":
        Patient_ID = request.user.id
        PatientName = request.user.first_name + request.user.last_name
        Department = request.POST['Department']
        doctor = request.POST['doctor']
        DoctorID = doctor.split()[0]
        DoctorEmail = doctor.split()[1]
        DoctorName = doctor.split()[2]
        DoctorSurname = doctor.split()[3]
        Symptoms = request.POST['Symptoms']
        Date = request.POST['Date']
        time = request.POST['Time']
        comment = request.POST['comment']

        try:
            Appoitment.objects.create(Patient_ID_id=Patient_ID, PatientName=PatientName, Doctor_ID_id=DoctorID, DoctorEmail=DoctorEmail, symptoms=Symptoms,
                                      department=Department, appoitmentDate=Date, appoitmentTime=time, Comments=comment)

            template = render_to_string(
                'email_booking.html', {'PatientName': PatientName, 'DoctorName': DoctorName, 'DoctorSurname': DoctorSurname, 'Date': Date, 'time': time})
            send_mail(
                'Hello there ' + PatientName,
                template,
                settings.EMAIL_HOST_USER,
                ['namew34997@mxclip.com'],
                fail_silently=False,
            )
            return render(request, 'conformation.html', {'PatientName': PatientName, 'DoctorName': DoctorName, 'DoctorSurname': DoctorSurname, 'Date': Date, 'time': time, 'DoctorEmail': DoctorEmail})
        except Exception as e:
            messages.success(
                request, ("Looks like a field is empty"))
    return render(request, 'booking.html', d)


def delete_appointment(request, aid):
    appoitment = Appoitment.objects.get(id=aid)
    appoitment.delete()
    g = request.user.groups.all()[0].name
    if g == 'Patient':
        return redirect('userProfile')
    else:
        return redirect('doctorProfile')


def userProfile(request):
    upcomming_appointments = Appoitment.objects.all().filter(
        Patient_ID=request.user, appoitmentDate__gte=timezone.now()).order_by('appoitmentDate')
    past_appointments = Appoitment.objects.all().filter(
        Patient_ID=request.user, appoitmentDate__lt=timezone.now()).order_by('-appoitmentDate')
    g = request.user.groups.all()[0].name
    if g == 'Patient':
        patient_details = Patient.objects.all().filter(EmailAddress=request.user)
        d = {'patient_details': patient_details,
             'upcomming_appointments': upcomming_appointments,
             'past_appointments': past_appointments}
    return render(request, 'userProfile.html', d)


def doctorProfile(request):
    upcomming_appointments = Appoitment.objects.all().filter(
        DoctorEmail=request.user, appoitmentDate__gte=timezone.now()).order_by('appoitmentDate')
    past_appointments = Appoitment.objects.all().filter(
        DoctorEmail=request.user, appoitmentDate__lt=timezone.now()).order_by('-appoitmentDate')
    g = request.user.groups.all()[0].name
    if g == 'Doctors':
        doctor_details = Doctor.objects.all().filter(EmailAddress=request.user)
        d = {'doctor_details': doctor_details,
             'upcomming_appointments': upcomming_appointments,
             'past_appointments': past_appointments}
    return render(request, 'doctorProfile.html', d)


def doctors(request):

    docs = Doctor.objects.all()

    return render(request, 'doctors.html', {'docs': docs})


def doctorlogin(request):
    if request.method == "POST":
        u = request.POST['Username']
        p = request.POST['Password']

        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            g = request.user.groups.all()[0].name
            if g == 'Doctors':
                doctor_details = Doctor.objects.all().filter(EmailAddress=request.user)
                d = {'doctor_details': doctor_details}
                return redirect('doctorProfile')
            if g == 'Patient':
                messages.success(
                    request, ("You cannot login with patient's detail. Do so from patient login or login with doctor's details"))
                auth.logout(request)
                return redirect('doclogin')
        else:
            messages.success(
                request, ("Invalid username or password. Please try again.."))
            return redirect('doclogin')
    else:
        return render(request, 'doctorlogin.html')


def loginPage(request):
    if request.method == "POST":
        u = request.POST['EmailAddress']
        p = request.POST['Password']

        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            g = request.user.groups.all()[0].name
            if g == 'Patient':
                patient_details = Patient.objects.all().filter(EmailAddress=request.user)
                d = {'patient_details': patient_details}
                return redirect('userProfile')
            if g == 'Doctors':
                messages.success(
                    request, ("You cannot login with Doctors's detail. Do so from Doctor login or login with patients's details"))
                auth.logout(request)
                return redirect('login')
        else:
            messages.success(
                request, ("Invalid username or password. Please try again.."))
            return redirect('login')
    else:
        return render(request, 'login.html')


def help(request):
    Help_details = Help.objects.all()
    d = {'Help_details': Help_details}
    return render(request, 'help.html', d)


def signup(request):
    user = "none"
    if request.method == "POST":
        FirstName = request.POST['FirstName']
        LastName = request.POST['LastName']
        image = request.FILES['image']
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
                Patient.objects.create(FirstName=FirstName, LastName=LastName, image=image, age=age, gender=gender,
                                       address=address, PhoneNumber=PhoneNumber, EmailAddress=EmailAddress, BloodGroup=BloodGroup)
                user = User.objects.create_user(
                    first_name=FirstName, last_name=LastName, email=EmailAddress, password=Password, username=EmailAddress)
                pat_group = Group.objects.get(name="Patient")
                pat_group.user_set.add(user)
                user.save()
                return redirect('login')
            else:
                messages.success(
                    request, ("Passwords do not match. Please try again"))
        except Exception as e:
            messages.success(
                request, ("This email already exists. Try again with another email or recover your account"))
    return render(request, 'signup.html')


def conformation(request):
    return render(request, 'conformation.html')


def logout(request):
    auth.logout(request)
    return redirect('/')
