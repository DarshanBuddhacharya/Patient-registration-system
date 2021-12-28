from PIL import Image
from django.db import models

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

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     image = Image.open(self.image.path)

    #     if image.height > 500 or image.weight > 500:
    #         output_size = (500, 500)
    #         image.thumbnail(output_size)
    #         image.save(self.image.path)

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

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     img = Image.open(self.img.path)

    #     if img.height > 500 or img.weight > 500:
    #         output_size = (500, 500)
    #         img.thumbnail(output_size)
    #         img.save(self.img.path)

    def __str__(self):
        return self.name
