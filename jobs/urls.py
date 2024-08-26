from django.urls import path,include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'jobs', JobViewSet, basename='job'),
router.register(r'job-applications', JobApplicationViewSet, basename='job-application')
router.register(r'employer/job-applications', EmployerJobApplicationViewSet, basename='employer-job-applications')


urlpatterns = [
    path('', include(router.urls)),
    path('apply/', JobApplicationCreateView.as_view(), name='job-application-create'),

]

