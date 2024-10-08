# Generated by Django 5.1 on 2024-08-23 18:53

import accounts.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_employer_logo_alter_jobseeker_pic_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employer',
            name='uuid',
            field=models.CharField(blank=True, max_length=8, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='employer',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to=accounts.utils.get_company_logos_path),
        ),
        migrations.AlterField(
            model_name='jobseeker',
            name='pic',
            field=models.ImageField(blank=True, null=True, upload_to=accounts.utils.get_profile_pictures_path, verbose_name='Profile Picture'),
        ),
        migrations.AlterField(
            model_name='jobseeker',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to=accounts.utils.get_resume_path, verbose_name='Resume'),
        ),
    ]
