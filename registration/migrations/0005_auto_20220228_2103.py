# Generated by Django 3.2 on 2022-02-28 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_appoitment_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='description',
            field=models.CharField(default=1, max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='department',
            name='img',
            field=models.ImageField(default='doc-2.jpg', upload_to='images'),
        ),
    ]
