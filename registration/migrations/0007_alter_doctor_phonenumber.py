# Generated by Django 3.2 on 2021-12-28 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_alter_doctor_phonenumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='phoneNumber',
            field=models.CharField(max_length=30),
        ),
    ]