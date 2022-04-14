# Generated by Django 3.2 on 2022-04-14 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0016_delete_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=100)),
                ('phoneNumber', models.CharField(max_length=15)),
                ('feedback', models.CharField(max_length=50)),
            ],
        ),
    ]
