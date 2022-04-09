# Generated by Django 3.2 on 2022-03-20 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0007_bloodreport'),
    ]

    operations = [
        migrations.CreateModel(
            name='MRIReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PatientEmail', models.CharField(max_length=100)),
                ('PatientName', models.CharField(max_length=100)),
                ('Date', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='images')),
                ('result', models.CharField(max_length=100)),
                ('Appoitment_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.appoitment')),
                ('Patient_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.patient')),
            ],
        ),
    ]