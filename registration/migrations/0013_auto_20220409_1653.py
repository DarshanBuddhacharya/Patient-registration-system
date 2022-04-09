# Generated by Django 3.2 on 2022-04-09 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0012_xrayreport'),
    ]

    operations = [
        migrations.AddField(
            model_name='xrayreport',
            name='normalPercent',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='xrayreport',
            name='pneoPercent',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
