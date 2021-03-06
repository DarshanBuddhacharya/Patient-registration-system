import requests
import json
from django.http import HttpResponse, JsonResponse
from xhtml2pdf import pisa

from time import timezone
from django.contrib import auth
from django.core.checks import messages
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
from keras.preprocessing.image import load_img, img_to_array
from django.core.files.storage import FileSystemStorage
import numpy as np
from keras.models import load_model
from tensorflow.keras.preprocessing import image
from django import template


def navbar(request):
    g = request.user.groups.all()[0].name
    if g == 'Doctor':
        doctor_details = Doctor.objects.all().filter(EmailAddress=request.user)
        d = {'doctor_details': doctor_details}
    if g == 'Patient':
        patient_details = Patient.objects.all().filter(EmailAddress=request.user)
        d = {'patient_details': patient_details}

    return render(request, 'navbar.html', d)


def index(request):
    return render(request, 'index.html')


def aboutus(request):
    return render(request, 'aboutus.html')


def contact(request):
    if request.method == "POST":
        FirstName = request.POST['FirstName']
        LastName = request.POST['LastName']
        EmailAddress = request.POST['EmailAddress']
        Phonenumber = request.POST['Phonenumber']
        userfeedback = request.POST['feedback']
        name = FirstName + ' ' + LastName

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
            Feedback.objects.create(
                name=name, email=EmailAddress, phoneNumber=Phonenumber, feedback=userfeedback)
            return redirect('home')
        except Exception as e:
            raise e
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
        patient_details = Patient.objects.all().filter(EmailAddress=request.user.email)
        d = {'patient_details': patient_details,
             'doctor_details': doctor_details,
             'department_details': department_details}

    if request.method == "POST":
        Patient_ID = request.POST['PatientID']
        PatientEmail = request.user.email
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


def docBooking(request, aid):
    if not request.user.is_active:
        messages.success(
            request, ("In order to book an appointment you must login first"))
        return redirect('login')
    doctor_details = Doctor.objects.all().filter(id=aid)
    department_details = Department.objects.all()
    g = request.user.groups.all()[0].name
    if g == 'Patient':
        patient_details = Patient.objects.all().filter(EmailAddress=request.user.email)
        d = {'patient_details': patient_details,
             'doctor_details': doctor_details,
             'department_details': department_details}

    if request.method == "POST":
        Patient_ID = request.POST['PatientID']
        PatientEmail = request.user.email
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
    return render(request, 'docBooking.html', d)


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


def delete_user(request):
    patient_details = Patient.objects.filter(EmailAddress=request.user.email)
    user_patient = User.objects.filter(email=request.user.email)
    patient_details = Patient.objects.filter(
        EmailAddress=request.user.email)
    d = {'patient_details': patient_details}
    template = render_to_string(
        'email/email_patient_delete.html', d)
    send_mail(
        'Account Deleted',
        template,
        settings.EMAIL_HOST_USER,
        [request.user.email],
        fail_silently=False,
    )
    patient_details.delete()
    user_patient.delete()
    messages.success(
        request, ("Your account was successfully deleted. We enjoyed your stay."))
    return redirect('home')


def userProfile(request):
    upcomming_appointments = Appoitment.objects.all().filter(
        PatientEmail=request.user.email, appoitmentDate__gte=timezone.now(), active="yes").order_by('appoitmentDate')
    past_appointments = Appoitment.objects.all().filter(
        PatientEmail=request.user.email, appoitmentDate__lt=timezone.now()).order_by('-appoitmentDate')
    completed_appointments = Appoitment.objects.all().filter(
        PatientEmail=request.user.email, appoitmentDate__gte=timezone.now(), active="no").order_by('appoitmentDate')
    report_details = MedicalReport.objects.all().filter(
        PatientEmail=request.user.email).order_by('-Date')
    bloodReport_details = BloodReport.objects.all().filter(
        PatientEmail=request.user.email)
    mriReport_details = MRIReport.objects.all().filter(
        PatientEmail=request.user.email)
    endoscopy_details = EndoscopyReport.objects.all().filter(
        PatientEmail=request.user.email)
    xray_details = XrayReport.objects.all().filter(
        PatientEmail=request.user.email)
    g = request.user.groups.all()[0].name
    if g == 'Patient':
        patient_details = Patient.objects.all().filter(EmailAddress=request.user.email)
        d = {'patient_details': patient_details,
             'upcomming_appointments': upcomming_appointments,
             'report_details': report_details,
             'completed_appointments': completed_appointments,
             'past_appointments': past_appointments,
             'bloodReport_details': bloodReport_details,
             'mriReport_details': mriReport_details,
             'endoscopy_details': endoscopy_details,
             'xray_details': xray_details}
    return render(request, 'userProfile.html', d)


def userEdit(request, aid):
    g = request.user.groups.all()[0].name
    if g == 'Patient':
        patient_details = Patient.objects.all().filter(EmailAddress=request.user.email)
        d = {'patient_details': patient_details}
    if request.method == "POST":
        image = request.FILES.get('image', "None")
        age = request.POST['age']
        gender = request.POST['gender']
        address = request.POST['address']
        PhoneNumber = request.POST['PhoneNumber']
        BloodGroup = request.POST['BloodGroup']
        try:
            patient = Patient.objects.get(pk=aid)
            if image != 'None':
                patient.image = image
            if age != '':
                patient.age = age
            if gender != 'non-binary':
                patient.gender = gender
            if address != '':
                patient.address = address
            if PhoneNumber != '':
                patient.PhoneNumber = PhoneNumber
            if BloodGroup != 'defult':
                patient.BloodGroup = BloodGroup
            patient.save()
            return redirect('userProfile')
        except Exception as e:
            raise e
    return render(request, 'userEdit.html', d)


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
    bloodReport_details = BloodReport.objects.all().filter(Appoitment_ID_id=aid)
    mriReport_details = MRIReport.objects.all().filter(Appoitment_ID_id=aid)
    endoscopy_details = EndoscopyReport.objects.all().filter(Appoitment_ID_id=aid)
    xray_details = XrayReport.objects.all().filter(Appoitment_ID_id=aid)
    d = {'appoitment_details': appoitment_details,
         'bloodReport_details': bloodReport_details,
         'mriReport_details': mriReport_details,
         'endoscopy_details': endoscopy_details,
         'xray_details': xray_details}

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
            template = render_to_string(
                'email/email_mediReport.html', {'PatientName': PatientName, 'DoctorFullName': DoctorFullName})
            send_mail(
                'Medical report Published,' + PatientName,
                template,
                settings.EMAIL_HOST_USER,
                [request.user.email],
                fail_silently=False,
            )
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
            messages.success(
                request, ("Lab report has been published. Doctor and patient can view the lab reports"))
            return redirect('labWorkshop')
        except Exception as e:
            raise e
    return render(request, 'labReports/bloodReport.html', d)


def endoscopyReport(request, aid):
    appoitment_details = Appoitment.objects.all().filter(id=aid)
    d = {'appoitment_details': appoitment_details}
    if request.method == "POST":
        Appoitment_ID = request.POST['SessionID']
        Patient_ID = request.POST['PatientID']
        PatientName = request.POST['PatientName']
        PatientEmail = request.POST['PatientEmail']
        Date = request.POST['Date']
        Fungus = request.POST['Fungus']
        Body = request.POST['Body']
        Antrum = request.POST['Antrum']
        P_ring = request.POST['P_ring']
        Bulb = request.POST['Bulb']
        Papilla = request.POST['Papilla']
        Oesophagus = request.POST['Oesophagus']
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
            EndoscopyReport.objects.create(Appoitment_ID_id=Appoitment_ID, Patient_ID_id=Patient_ID,
                                           PatientName=PatientName, Date=Date, PatientEmail=PatientEmail, Fungus=Fungus, Body=Body, Antrum=Antrum, P_ring=P_ring, Bulb=Bulb, Papilla=Papilla, Oesophagus=Oesophagus)
            messages.success(
                request, ("Lab report has been published. Doctor and patient can view the lab reports"))
            return redirect('labWorkshop')
        except Exception as e:
            raise e
    return render(request, 'labReports/endoscopyReport.html', d)


def get_img_array(img_path):
    path = img_path
    img = image.load_img(path, target_size=(224, 224, 3))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)

    return img


def tumor_pred(imageTumor):
    model = load_model("bestTumor.sav")
    fs = FileSystemStorage()
    filePathName = fs.save(imageTumor.name, imageTumor)
    filePathName = fs.url(filePathName)
    path = '.'+filePathName
    class_type = {0: 'Healthy',  1: 'Tumor'}
    img = get_img_array(path)

    res = class_type[np.argmax(model.predict(img))]
    normalPercent = model.predict(img)[0][0]*100
    tumorPercent = model.predict(img)[0][1]*100
    return res, normalPercent, tumorPercent


def pneo_pred(imagePneo):
    model = load_model("bestPneo2.sav")
    fs = FileSystemStorage()
    filePathName = fs.save(imagePneo.name, imagePneo)
    filePathName = fs.url(filePathName)
    path = '.'+filePathName
    class_type = {0: 'Normal', 1: 'Pneumonia'}
    img = get_img_array(path)

    res = class_type[np.argmax(model.predict(img))]
    normalPercent = model.predict(img)[0][0]*100
    pneoPercent = model.predict(img)[0][1]*100
    return res, normalPercent, pneoPercent


def mriReport(request, aid):
    appoitment_details = Appoitment.objects.all().filter(id=aid)
    if request.method == "POST":
        Appoitment_ID = request.POST['SessionID']
        Patient_ID = request.POST['PatientID']
        PatientName = request.POST['PatientName']
        PatientEmail = request.POST['PatientEmail']
        Date = request.POST['Date']
        imageTumor = request.FILES['imageTumor']

        result, normalPercent, tumorPercent = tumor_pred(imageTumor)
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
            MRIReport.objects.create(Appoitment_ID_id=Appoitment_ID, Patient_ID_id=Patient_ID,
                                     PatientName=PatientName, Date=Date, PatientEmail=PatientEmail, image=imageTumor, result=result, normalPercent=normalPercent, tumorPercent=tumorPercent)
            messages.success(
                request, ("Lab report has been published. Doctor and patient can view the lab reports"))
            return redirect('labWorkshop')
        except Exception as e:
            raise e
    return render(request, 'labReports/MRIReport.html', {'appoitment_details': appoitment_details})


def xrayReport(request, aid):
    appoitment_details = Appoitment.objects.all().filter(id=aid)
    if request.method == "POST":
        Appoitment_ID = request.POST['SessionID']
        Patient_ID = request.POST['PatientID']
        PatientName = request.POST['PatientName']
        PatientEmail = request.POST['PatientEmail']
        Date = request.POST['Date']
        imagePneo = request.FILES['imagePneo']

        result, normalPercent, pneoPercent = pneo_pred(imagePneo)
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
            XrayReport.objects.create(Appoitment_ID_id=Appoitment_ID, Patient_ID_id=Patient_ID,
                                      PatientName=PatientName, Date=Date, PatientEmail=PatientEmail, image=imagePneo, result=result, normalPercent=normalPercent, pneoPercent=pneoPercent)
            messages.success(
                request, ("Lab report has been published. Doctor and patient can view the lab reports"))
            return redirect('labWorkshop')
        except Exception as e:
            raise e
    return render(request, 'labReports/XrayReport.html', {'appoitment_details': appoitment_details})


def render_pdf_view(request, aid):
    template_path = 'printing/reportPrint.html'
    report_context = MedicalReport.objects.all().filter(id=aid)
    context = {'report_context': report_context}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
        html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def render_pdf_blood(request, aid):
    template_path = 'printing/bloodReportPrint.html'
    report_context = BloodReport.objects.all().filter(id=aid)
    context = {'report_context': report_context}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
        html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def render_pdf_endoscopy(request, aid):
    template_path = 'printing/endoscopyReportPrint.html'
    report_context = EndoscopyReport.objects.all().filter(id=aid)
    context = {'report_context': report_context}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
        html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def render_pdf_Mri(request, aid):
    template_path = 'printing/mriReportPrint.html'
    report_context = MRIReport.objects.all().filter(id=aid)
    context = {'report_context': report_context}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
        html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def render_pdf_Xray(request, aid):
    template_path = 'printing/xrayReportPrint.html'
    report_context = XrayReport.objects.all().filter(id=aid)
    context = {'report_context': report_context}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
        html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def is_valid_queryparam(param):
    return param != '' and param is not None


def search_doc(request):
    qs = Doctor.objects.filter()
    serName = request.GET.get('serName')
    serDep = request.GET.get('serDep')
    serEdu = request.GET.get('serEdu')
    serExp = request.GET.get('serExp')
    serHos = request.GET.get('serHos')

    if is_valid_queryparam(serName):
        qs = qs.filter(name__icontains=serName)

    elif is_valid_queryparam(serDep):
        qs = qs.filter(speciality__name__icontains=serDep)

    elif is_valid_queryparam(serEdu):
        qs = qs.filter(education__icontains=serEdu)

    elif is_valid_queryparam(serExp):
        qs = qs.filter(experince__gte=serExp)

    elif is_valid_queryparam(serHos):
        qs = qs.filter(hospital__icontains=serHos)

    return qs


def search_docBook(request, aid):
    qs = Doctor.objects.all().filter(speciality_id=aid)
    serName = request.GET.get('serName')
    serEdu = request.GET.get('serEdu')
    serExp = request.GET.get('serExp')
    serHos = request.GET.get('serHos')

    if is_valid_queryparam(serName):
        qs = qs.filter(name__icontains=serName)

    elif is_valid_queryparam(serEdu):
        qs = qs.filter(education__icontains=serEdu)

    elif is_valid_queryparam(serExp):
        qs = qs.filter(experince__gte=serExp)

    elif is_valid_queryparam(serHos):
        qs = qs.filter(hospital__icontains=serHos)

    return qs


def search_patient(request):
    qe = Appoitment.objects.all().filter(
        appoitmentDate__gte=timezone.now(), active="yes").order_by('appoitmentDate')
    serName = request.GET.get('serName')
    serDep = request.GET.get('serDoc')

    if is_valid_queryparam(serName):
        qe = qe.filter(PatientName__icontains=serName)

    elif is_valid_queryparam(serDep):
        qe = qe.filter(DoctorFullName__icontains=serDep)

    return qe


def doctors(request):
    qs = search_doc(request)
    context = {
        'queryset': qs
    }

    return render(request, 'doctors.html', context)


def depDoctor(request, aid):
    qs = search_docBook(request, aid)
    context = {
        'queryset': qs
    }

    return render(request, 'depDoctor.html', context)


def labWorkshop(request):
    qe = search_patient(request)
    d = {'qe': qe}
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
                messages.success(
                    request, ("You are successfully loged in. Hello there."))
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
                messages.success(
                    request, ("You are successfully loged in. Hello there Doctor"))
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
                # patient_details = Patient.objects.all().filter(EmailAddress=request.user)
                # d = {'patient_details': patient_details}
                messages.success(
                    request, ("You are successfully loged in. Welcome to Dhanvantari"))
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
        image = request.FILES.get('image')
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
                messages.success(
                    request, ("Your account was successfully Created. Welcome to Dhanvantari."))
                return redirect('login')
            else:
                messages.success(
                    request, ("Passwords do not match. Please try again"))
        except Exception as e:
            messages.success(
                request, ("This email already exists. Try again with another email or recover your account"))
    return render(request, 'signup.html')


def socialSignup(request):
    if request.method == "POST":
        FirstName = request.user.first_name
        LastName = request.user.last_name
        image = request.FILES.get('image')
        age = request.POST['age']
        gender = request.POST['gender']
        address = request.POST['address']
        PhoneNumber = request.POST['PhoneNumber']
        EmailAddress = request.user.email
        BloodGroup = request.POST['BloodGroup']

        try:
            Patient.objects.create(FirstName=FirstName, LastName=LastName, image=image, age=age, gender=gender,
                                   address=address, PhoneNumber=PhoneNumber, EmailAddress=EmailAddress, BloodGroup=BloodGroup)
            user = request.user
            pat_group = Group.objects.get(name="Patient")
            pat_group.user_set.add(user)
            user.save()
            return redirect('userProfile')
        except Exception as e:
            raise e
    patient_details = Patient.objects.all().filter(EmailAddress=request.user.email)
    d = {'patient_details': patient_details}
    return render(request, 'socialSignup.html', d)


def conformation(request):
    return render(request, 'conformation.html')


def logout(request):
    messages.success(
        request, ("Successfully logged out. See you next time."))
    auth.logout(request)
    return redirect('/')


def footer(request):
    if request.method == "POST":
        EmailAddress = request.POST['EmailAddress']
        userfeedback = request.POST['feedback']
        try:
            Feedback.objects.create(
                email=EmailAddress, feedback=userfeedback)
            return redirect('home')
        except Exception as e:
            raise e
    return render(request, 'footer.html')


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
