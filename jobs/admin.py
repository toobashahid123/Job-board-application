from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Job)
class StandardAdmin(admin.ModelAdmin):
    list_display = ['id','title','posted_by','description','company','location']

@admin.register(JobApplication)
class StandardAdmin(admin.ModelAdmin):
    list_display = ['id','job','applicant','cover_letter','resume','status']