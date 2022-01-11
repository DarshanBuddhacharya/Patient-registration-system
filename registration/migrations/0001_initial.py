# Generated by Django 3.2 on 2021-12-08 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FirstName', models.CharField(max_length=50)),
                ('LastName', models.CharField(max_length=50)),
                ('age', models.CharField(max_length=30)),
                ('gender', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=100)),
                ('PhoneNumber', models.CharField(max_length=15)),
                ('EmailAddress', models.EmailField(max_length=254, unique=True)),
                ('Password', models.CharField(max_length=50)),
                ('RepeatPassword', models.CharField(max_length=50)),
                ('BloodGroup', models.CharField(max_length=5)),
            ],
        ),
    ]