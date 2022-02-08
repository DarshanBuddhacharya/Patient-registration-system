# Generated by Django 3.2 on 2022-02-08 06:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appoitment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PatientName', models.CharField(max_length=100)),
                ('DoctorFullName', models.CharField(max_length=100)),
                ('DoctorEmail', models.CharField(max_length=100)),
                ('department', models.CharField(choices=[('ENT (Ear-Nose-Throat)', 'ENT (Ear-Nose-Throat)'), ('Ophthalmologists', 'OPHTHALMOLOGISTS'), ('Neurologists', 'NEUROLOGISTS'), ('pulmonologists', 'PULMONOLOGISTS')], default='General', max_length=100)),
                ('symptoms', models.CharField(max_length=500)),
                ('appoitmentDate', models.DateField()),
                ('appoitmentTime', models.TimeField()),
                ('Comments', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('img', models.ImageField(upload_to='images')),
                ('speciality', models.CharField(choices=[('ENT (Ear-Nose-Throat)', 'ENT (Ear-Nose-Throat)'), ('Ophthalmologists', 'OPHTHALMOLOGISTS'), ('Neurologists', 'NEUROLOGISTS'), ('pulmonologists', 'PULMONOLOGISTS')], default='General', max_length=100)),
                ('education', models.CharField(max_length=50)),
                ('gender', models.CharField(choices=[('male', 'MALE'), ('female', 'FEMALE'), ('other', 'OTHER')], default='male', max_length=10)),
                ('age', models.IntegerField()),
                ('availableFrom', models.TimeField()),
                ('availableTo', models.TimeField()),
                ('phoneNumber', models.CharField(max_length=30)),
                ('EmailAddress', models.EmailField(max_length=254, unique=True)),
                ('experince', models.IntegerField()),
                ('hospital', models.CharField(max_length=100)),
                ('facebook', models.CharField(blank=True, max_length=1000)),
                ('instragram', models.CharField(blank=True, max_length=1000)),
                ('twitter', models.CharField(blank=True, max_length=1000)),
                ('linkedin', models.CharField(blank=True, max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Help',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=50)),
                ('Description', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FirstName', models.CharField(max_length=50)),
                ('LastName', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='images')),
                ('age', models.CharField(max_length=30)),
                ('gender', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=100)),
                ('PhoneNumber', models.CharField(max_length=15)),
                ('EmailAddress', models.EmailField(max_length=254, unique=True)),
                ('BloodGroup', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='MedicalReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PatientName', models.CharField(max_length=100)),
                ('DoctorFullName', models.CharField(max_length=100)),
                ('DoctorEmail', models.CharField(max_length=100)),
                ('department', models.CharField(choices=[('ENT (Ear-Nose-Throat)', 'ENT (Ear-Nose-Throat)'), ('Ophthalmologists', 'OPHTHALMOLOGISTS'), ('Neurologists', 'NEUROLOGISTS'), ('pulmonologists', 'PULMONOLOGISTS')], default='General', max_length=100)),
                ('DiagnosisReport', models.CharField(max_length=800)),
                ('DoctorComments', models.CharField(max_length=500)),
                ('MorningMedicine', models.CharField(max_length=100)),
                ('DayMedicine', models.CharField(max_length=100)),
                ('NoonMedicine', models.CharField(max_length=100)),
                ('NightMedicine', models.CharField(max_length=100)),
                ('Appoitment_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.appoitment')),
                ('Doctor_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.doctor')),
                ('Patient_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.patient')),
            ],
        ),
        migrations.AddField(
            model_name='appoitment',
            name='Doctor_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.doctor'),
        ),
        migrations.AddField(
            model_name='appoitment',
            name='Patient_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.patient'),
        ),
    ]
