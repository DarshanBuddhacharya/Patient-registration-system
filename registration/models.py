from django.db import models

# Create your models here.


class Patient(models.Model):
    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(max_length=50)
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


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='images')
    speciality = models.CharField(max_length=100)
    education = models.CharField(max_length=50)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, default='male')
    age = models.IntegerField()
    availableFrom = models.CharField(max_length=30)
    availableTo = models.CharField(max_length=30)
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
