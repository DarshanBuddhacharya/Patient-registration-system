from unicodedata import name
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Patient(models.Model):
    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images')
    age = models.CharField(max_length=30)
    gender = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    PhoneNumber = models.CharField(max_length=15)
    EmailAddress = models.EmailField(unique=True)
    BloodGroup = models.CharField(max_length=5)

    def __str__(self):
        return self.FirstName


GENDER_CHOICES = (
    ('male', 'MALE'),
    ('female', 'FEMALE'),
    ('other', 'OTHER')
)

DEPARTMENT_CHOICES = (
    ('ENT (Ear-Nose-Throat)', 'ENT (Ear-Nose-Throat)'),
    ('Ophthalmologists', 'OPHTHALMOLOGISTS'),
    ('Neurologists', 'NEUROLOGISTS'),
    ('pulmonologists', 'PULMONOLOGISTS'),
)


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='images')
    speciality = models.ForeignKey(Department, on_delete=models.CASCADE)
    education = models.CharField(max_length=50)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, default='male')
    age = models.IntegerField()
    availableFrom = models.TimeField()
    availableTo = models.TimeField()
    phoneNumber = models.CharField(max_length=30)
    EmailAddress = models.EmailField(unique=True)
    experince = models.IntegerField()
    hospital = models.CharField(max_length=100)
    facebook = models.CharField(max_length=1000, blank=True)
    instragram = models.CharField(max_length=1000, blank=True)
    twitter = models.CharField(max_length=1000, blank=True)
    linkedin = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.name


class Appoitment(models.Model):
    Patient_ID = models.ForeignKey(Patient, on_delete=models.CASCADE)
    PatientEmail = models.CharField(max_length=100)
    PatientName = models.CharField(max_length=100)
    Doctor_ID = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    DoctorFullName = models.CharField(max_length=100)
    DoctorEmail = models.CharField(max_length=100)
    department = models.CharField(
        max_length=100, choices=DEPARTMENT_CHOICES, default='General')
    symptoms = models.CharField(max_length=500)
    appoitmentDate = models.DateField()
    appoitmentTime = models.TimeField()
    Comments = models.CharField(max_length=500)

    def __int__(self):
        return self.Doctor_ID + " has an appointment with " + self.Patient_ID


class MedicalReport(models.Model):
    Appoitment_ID = models.ForeignKey(Appoitment, on_delete=models.CASCADE)
    Patient_ID = models.ForeignKey(Patient, on_delete=models.CASCADE)
    PatientEmail = models.CharField(max_length=100)
    PatientName = models.CharField(max_length=100)
    Doctor_ID = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    DoctorFullName = models.CharField(max_length=100)
    DoctorEmail = models.CharField(max_length=100)
    Date = models.CharField(max_length=100)
    department = models.CharField(
        max_length=100, choices=DEPARTMENT_CHOICES, default='General')
    DiagnosisReport = models.CharField(max_length=800)
    DoctorComments = models.CharField(max_length=500)
    MorningMedicine = models.CharField(max_length=100)
    DayMedicine = models.CharField(max_length=100)
    NoonMedicine = models.CharField(max_length=100)
    NightMedicine = models.CharField(max_length=100)

    def __int__(self):
        return self.Doctor_ID + " has uploaded medical report of " + self.Patient_ID


class Help(models.Model):
    Title = models.CharField(max_length=50)
    Description = models.CharField(max_length=500)
