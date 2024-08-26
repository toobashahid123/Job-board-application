from rest_framework.routers import DefaultRouter
from django.db import router
from django.urls import path,include  
from .views import *
from rest_framework_simplejwt.views import TokenVerifyView

router = DefaultRouter()
router.register('all-user', AllUsersViewset, basename = 'users'),
router.register('employer/update', EmployerViewSet, basename = 'employer'),
router.register('jobseeker/update', JobseekerViewSet, basename = 'jobseeker'),


urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserSignUp.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    # path('delete-account/', DeleteUserView.as_view(), name='delete-account'),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
