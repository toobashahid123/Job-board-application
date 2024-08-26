from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
import os
from .utils import *

class User(AbstractUser):
    ROLE_CHOICES = [
        ('employer', 'Employer'),
        ('jobseeker', 'Jobseeker'),
    ]

    role = models.CharField(max_length=50, choices=ROLE_CHOICES, null=True, blank=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=False, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        app_label = 'accounts'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class JobSeeker(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobseeker', blank=True, null=True)
    uuid = models.CharField(max_length=8, unique=True, blank=True, null=True)
    name = models.CharField("Name of user", blank=True, null=True, max_length=255, default="")
    email = models.EmailField(max_length=200, blank=True, null=True)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, null=True, blank=True, default=None)
    pic = models.ImageField(('Profile Picture'), upload_to=get_profile_pictures_path, null=True, blank=True)
    phone_number = models.CharField(max_length=200, blank=True, null=True)
    qualification = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    resume = models.FileField(('Resume'), upload_to=get_resume_path, null=True, blank=True)
    portfolio = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = generate_uuid()
        super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        # Delete associated user instance
        self.user.delete()
        super().delete(*args, **kwargs)


class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer')
    uuid = models.CharField(max_length=8, unique=True, blank=True, null=True)
    company_name = models.CharField(max_length=255,blank=False)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to=get_company_logos_path, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = generate_uuid()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.company_name

    
         