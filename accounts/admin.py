from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username','role','email']


@admin.register(JobSeeker)
class StandardAdmin(admin.ModelAdmin):
    list_display = ['id','user','resume','created','updated']

@admin.register(Employer)
class StandardAdmin(admin.ModelAdmin):
    list_display = ['id','user','website','created','updated','logo']
        
        