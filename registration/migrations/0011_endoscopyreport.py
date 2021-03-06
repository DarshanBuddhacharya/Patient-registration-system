# Generated by Django 3.2 on 2022-04-08 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0010_alter_mrireport_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='EndoscopyReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PatientEmail', models.CharField(max_length=100)),
                ('PatientName', models.CharField(max_length=100)),
                ('Date', models.CharField(max_length=100)),
                ('Fungus', models.CharField(max_length=50)),
                ('Body', models.CharField(max_length=50)),
                ('Antrum', models.CharField(max_length=50)),
                ('P_ring', models.CharField(max_length=50)),
                ('Bulb', models.CharField(max_length=50)),
                ('Papilla', models.CharField(max_length=50)),
                ('Oesophagus', models.CharField(max_length=50)),
                ('Appoitment_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.appoitment')),
                ('Patient_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.patient')),
            ],
        ),
    ]
