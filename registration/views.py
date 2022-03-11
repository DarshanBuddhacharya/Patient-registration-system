import requests
import json
from django.http import HttpResponse, JsonResponse
from xhtml2pdf import pisa

from time import timezone
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
from django.template.loader import render_to_string, get_template
from django.views.decorators.csrf import csrf_exempt


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
    department_details = Department.objects.all()
    g = request.user.groups.all()[0].name
    if g == 'Patient':
        patient_details = Patient.objects.all().filter(EmailAddress=request.user)
        d = {'patient_details': patient_details,
             'doctor_details': doctor_details,
             'department_details': department_details}

    if request.method == "POST":
        Patient_ID = request.POST['PatientID']
        PatientEmail = request.user
        PatientName = request.user.first_name + request.user.last_name
        Speciality = request.POST['Department']
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
            template = render_to_string(
                'email/email_booking.html', {'PatientName': PatientName, 'DoctorName': DoctorName, 'DoctorSurname': DoctorSurname, 'Date': Date, 'time': time})
            send_mail(
                'Hello there ' + PatientName,
                template,
                settings.EMAIL_HOST_USER,
                [request.user.email],
                fail_silently=False,
            )
            Appoitment.objects.create(Patient_ID_id=Patient_ID, PatientName=PatientName, PatientEmail=PatientEmail, Doctor_ID_id=DoctorID, DoctorFullName=DoctorName + " " + DoctorSurname, DoctorEmail=DoctorEmail, symptoms=Symptoms,
                                      department=Speciality, appoitmentDate=Date, appoitmentTime=time, Comments=comment)
            return render(request, 'conformation.html', {'PatientName': PatientName, 'DoctorName': DoctorName, 'DoctorSurname': DoctorSurname, 'Date': Date, 'time': time, 'DoctorEmail': DoctorEmail})
        except Exception as e:
            raise e
            # messages.success(
            #     request, ("Looks like a field is empty"))
    return render(request, 'booking.html', d)


def load_doctor(request):
    department_id = request.GET.get('Department_id')
    doctors = Doctor.objects.all().filter(speciality=department_id).order_by('name')
    return render(request, 'doctor_dropdown.html', {'doctors': doctors})


def delete_appointment(request, aid):
    appoitment = Appoitment.objects.get(id=aid)
    g = request.user.groups.all()[0].name
    if g == 'Patient':
        appoitment_details = Appoitment.objects.all().filter(id=aid)
        d = {'appoitment_details': appoitment_details}
        template = render_to_string(
            'email/email_patient_cancel.html', d)
        send_mail(
            'Appoitment canceled',
            template,
            settings.EMAIL_HOST_USER,
            [request.user.email],
            fail_silently=False,
        )
        appoitment.delete()
        return redirect('userProfile')
    else:
        appoitment_details = Appoitment.objects.all().filter(id=aid)
        d = {'appoitment_details': appoitment_details}
        template = render_to_string(
            'email/email_doctor_cancel.html', d)
        send_mail(
            'Appoitment canceled',
            template,
            settings.EMAIL_HOST_USER,
            [request.user.email],
            fail_silently=False,
        )
        appoitment.delete()
        return redirect('doctorProfile')


def userProfile(request):
    upcomming_appointments = Appoitment.objects.all().filter(
        PatientEmail=request.user, appoitmentDate__gte=timezone.now(), active="yes").order_by('appoitmentDate')
    past_appointments = Appoitment.objects.all().filter(
        PatientEmail=request.user, appoitmentDate__lt=timezone.now()).order_by('-appoitmentDate')
    completed_appointments = Appoitment.objects.all().filter(
        PatientEmail=request.user, appoitmentDate__gte=timezone.now(), active="no").order_by('appoitmentDate')
    report_details = MedicalReport.objects.all().filter(
        PatientEmail=request.user).order_by('-Date')
    g = request.user.groups.all()[0].name
    if g == 'Patient':
        patient_details = Patient.objects.all().filter(EmailAddress=request.user)
        d = {'patient_details': patient_details,
             'upcomming_appointments': upcomming_appointments,
             'report_details': report_details,
             'completed_appointments': completed_appointments,
             'past_appointments': past_appointments}
    return render(request, 'userProfile.html', d)


def doctorProfile(request):
    upcomming_appointments = Appoitment.objects.all().filter(
        DoctorEmail=request.user, appoitmentDate__gte=timezone.now(), active="yes").order_by('appoitmentDate')
    past_appointments = Appoitment.objects.all().filter(
        DoctorEmail=request.user, appoitmentDate__lt=timezone.now()).order_by('-appoitmentDate')
    completed_appointments = Appoitment.objects.all().filter(
        DoctorEmail=request.user, appoitmentDate__gte=timezone.now(), active="no").order_by('appoitmentDate')
    report_details = MedicalReport.objects.all().filter(
        DoctorEmail=request.user).order_by('-Date')
    g = request.user.groups.all()[0].name
    if g == 'Doctor':
        doctor_details = Doctor.objects.all().filter(EmailAddress=request.user)
        d = {'doctor_details': doctor_details,
             'upcomming_appointments': upcomming_appointments,
             'past_appointments': past_appointments,
             'completed_appointments': completed_appointments,
             'report_details': report_details}
    if request.method == "POST":
        SessionID = request.POST['SessionID']
        editTime = request.POST['editTime']
        try:
            appoitment = Appoitment.objects.get(pk=SessionID)
            appoitment.appoitmentTime = editTime
            appoitment.save()
            appoitment_details = Appoitment.objects.all().filter(id=SessionID)
            d = {'appoitment_details': appoitment_details}
            template = render_to_string(
                'email/email_changeTime.html', d)
            send_mail(
                'Appoitment time changed_' + editTime,
                template,
                settings.EMAIL_HOST_USER,
                [request.user.email],
                fail_silently=False,
            )
            return redirect('doctorProfile')
        except Exception as e:
            raise e
    return render(request, 'doctorProfile.html', d)


def medicalReport(request, aid):
    appoitment_details = Appoitment.objects.all().filter(id=aid)
    d = {'appoitment_details': appoitment_details}
    if request.method == "POST":
        Appoitment_ID = request.POST['SessionID']
        Patient_ID = request.POST['PatientID']
        PatientName = request.POST['PatientName']
        PatientEmail = request.POST['PatientEmail']
        Doctor_ID = request.POST['DoctorID']
        Date = request.POST['Date']
        DoctorEmail = request.user.email
        DoctorFullName = request.user.first_name + " " + request.user.last_name
        Department = request.POST['department']
        DiagnosisReport = request.POST['DiagnosisReport']
        DoctorComments = request.POST['DoctorComments']
        MorningMedicine = request.POST['MorningMedicine']
        DayMedicine = request.POST['DayMedicine']
        NoonMedicine = request.POST['NoonMedicine']
        NightMedicine = request.POST['NightMedicine']
        active = request.POST['active']
        try:
            # template = render_to_string(
            #     'email/email_booking.html', {'PatientName': PatientName, 'DoctorFullName': DoctorFullName, 'Date': d.Date, 'time': d.time})
            # send_mail(
            #     'Hello there ' + PatientName,
            #     template,
            #     settings.EMAIL_HOST_USER,
            #     [request.user.email],
            #     fail_silently=False,
            # )
            MedicalReport.objects.create(Appoitment_ID_id=Appoitment_ID, Patient_ID_id=Patient_ID, PatientName=PatientName, Doctor_ID_id=Doctor_ID, DoctorFullName=DoctorFullName, DoctorEmail=DoctorEmail, DiagnosisReport=DiagnosisReport,
                                         department=Department, Date=Date, PatientEmail=PatientEmail, DoctorComments=DoctorComments, MorningMedicine=MorningMedicine, DayMedicine=DayMedicine, NoonMedicine=NoonMedicine, NightMedicine=NightMedicine)
            appoitment = Appoitment.objects.get(pk=Appoitment_ID)
            appoitment.active = active
            appoitment.save()
            return redirect('doctorProfile')
        except Exception as e:
            raise e
    return render(request, 'medicalReport.html', d)


def bloodReport(request, aid):
    appoitment_details = Appoitment.objects.all().filter(id=aid)
    d = {'appoitment_details': appoitment_details}
    if request.method == "POST":
        Appoitment_ID = request.POST['SessionID']
        Patient_ID = request.POST['PatientID']
        PatientName = request.POST['PatientName']
        PatientEmail = request.POST['PatientEmail']
        Date = request.POST['Date']
        RBCCount = request.POST['RBCCount']
        Hemoglobin = request.POST['Hemoglobin']
        Hematocrit = request.POST['Hematocrit']
        WBCcount = request.POST['WBCcount']
        Platelet = request.POST['Platelet']
        try:
            # template = render_to_string(
            #     'email/email_booking.html', {'PatientName': PatientName, 'DoctorFullName': DoctorFullName, 'Date': d.Date, 'time': d.time})
            # send_mail(
            #     'Hello there ' + PatientName,
            #     template,
            #     settings.EMAIL_HOST_USER,
            #     [request.user.email],
            #     fail_silently=False,
            # )
            BloodReport.objects.create(Appoitment_ID_id=Appoitment_ID, Patient_ID_id=Patient_ID,
                                       PatientName=PatientName, Date=Date, PatientEmail=PatientEmail, RBCCount=RBCCount, Hemoglobin=Hemoglobin, Hematocrit=Hematocrit, WBCcount=WBCcount, Platelet=Platelet)
            return redirect('labWorkshop')
        except Exception as e:
            raise e
    return render(request, 'bloodReport.html', d)


def render_pdf_view(request, aid):
    template_path = 'reportPrint.html'
    report_context = MedicalReport.objects.all().filter(id=aid)
    context = {'report_context': report_context}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def doctors(request):

    docs = Doctor.objects.all()

    return render(request, 'doctors.html', {'docs': docs})


def labWorkshop(request):
    appointments = Appoitment.objects.all().filter(
        appoitmentDate__gte=timezone.now(), active="yes").order_by('appoitmentDate')
    d = {'appointments': appointments}
    return render(request, 'labWorkshop.html', d)


def labLogin(request):
    if request.method == "POST":
        u = request.POST['Username']
        p = request.POST['Password']

        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            g = request.user.groups.all()[0].name
            if g == 'Lab':
                return redirect('labWorkshop')
            if g == 'Patient':
                messages.success(
                    request, ("You cannot login with patient's detail. Do so from patient login or login with doctor's details"))
                auth.logout(request)
                return redirect('labLogin')
        else:
            messages.success(
                request, ("Invalid username or password. Please try again.."))
            return redirect('labLogin')
    else:
        return render(request, 'labLogin.html')


def department(request):
    deps = Department.objects.all()
    return render(request, 'department.html', {'deps': deps})


def doctorlogin(request):
    if request.method == "POST":
        u = request.POST['Username']
        p = request.POST['Password']

        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            g = request.user.groups.all()[0].name
            if g == 'Doctor':
                doctor_details = Doctor.objects.all().filter(EmailAddress=request.user)
                d = {'doctor_details': doctor_details}
                return redirect('doctorProfile')
            if g == 'Patient':
                messages.success(
                    request, ("You cannot login with patient's detail. Do so from patient login or login with doctor's details"))
                auth.logout(request)
                return redirect('doctorlogin')
        else:
            messages.success(
                request, ("Invalid username or password. Please try again.."))
            return redirect('doctorlogin')
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
            if g == 'Doctor':
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


@csrf_exempt
def verify_payment(request):
    data = request.POST
    product_id = data['product_identity']
    token = data['token']
    amount = data['amount']

    url = "https://khalti.com/api/v2/payment/verify/"
    payload = {
        "token": token,
        "amount": amount
    }
    headers = {
        "Authorization": "Key test_secret_key_6406136b79544ca68005ffe1265d3678"
    }

    response = requests.post(url, payload, headers=headers)

    response_data = json.loads(response.text)
    status_code = str(response.status_code)

    if status_code == '400':
        response = JsonResponse(
            {'status': 'false', 'message': response_data['detail']}, status=500)
        return response


def footer(request):
    return render(request, 'footer.html')
