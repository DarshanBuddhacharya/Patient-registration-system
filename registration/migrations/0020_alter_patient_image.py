# Generated by Django 3.2 on 2022-04-14 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0019_alter_patient_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='image',
            field=models.ImageField(upload_to='images'),
        ),
    ]
