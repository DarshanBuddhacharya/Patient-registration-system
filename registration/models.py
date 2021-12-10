from django.db import models

# Create your models here.


class Patient(models.Model):
    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(max_length=50)
    age = models.CharField(max_length=30)
    gender = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    PhoneNumber = models.CharField(max_length=15)
    EmailAddress = models.EmailField(unique=True)
    Password = models.CharField(max_length=50)
    RepeatPassword = models.CharField(max_length=50)
    BloodGroup = models.CharField(max_length=5)

    def __str__(self):
        return self.FirstName
