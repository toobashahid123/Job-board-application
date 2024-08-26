from django.shortcuts import render
from .models import *
from rest_framework import status,viewsets, generics
from rest_framework import filters
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import DestroyAPIView
from notifications.signals import send_welcome_email

# Create your views here.
class AllUsersViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AllUserProfileSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email',]
    http_method_names = ["get"]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserSignUp(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Send welcome email
            send_welcome_email(user)

            # Generate tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response_data = {
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "role": user.role,
                },
                "access_token": access_token,
                "refresh_token": refresh_token
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLogin(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                # Update the last login time
                update_last_login(None, user)
                
                # Generate tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                response_data = {
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "username": user.username,
                        "role": user.role,
                    },
                    "access_token": access_token,
                    "refresh_token": refresh_token
                }

                return Response(response_data, status=status.HTTP_200_OK)
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Successfully logged out'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class EmployerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployerSerializer
    http_method_names = ["get","put","patch","delete"]

    def get_queryset(self):
        # Restrict queryset to only the employer record of the currently authenticated user
        # if self.request.user.is_authenticated:
        #     return Employer.objects.filter(user=self.request.user)
        # return Employer.objects.none()
        if self.request.user.is_authenticated:
            return Employer.objects.all()
        return Employer.objects.none()
        
    
    def update(self, request, *args, **kwargs):
        employer_instance = self.get_object()

        # Ensure the authenticated user can only update their own profile
        if request.user != employer_instance.user:
            return Response({'detail': 'You can only update your own profile.'}, status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)
        

    def destroy(self, request, *args, **kwargs):
        employer_instance = self.get_object()

        # Ensure the authenticated user can only delete their own profile
        if request.user != employer_instance.user:
            return Response({'detail': 'You can only delete your own profile.'}, status=status.HTTP_403_FORBIDDEN)
        
        # Optionally, delete the associated User instance as well
        employer_instance.user.delete()
        return super().destroy(request, *args, **kwargs)
        

class JobseekerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = JobseekerSerializer
    http_method_names = ["get","put","patch","delete"]

    def get_queryset(self):
        # Restrict queryset to only the employer record of the currently authenticated user
        if self.request.user.is_authenticated:
            return JobSeeker.objects.all()
        return JobSeeker.objects.none()
        
    
    def update(self, request, *args, **kwargs):
        job_seeker_instance = self.get_object()

        # Ensure the authenticated user can only update their own profile
        if request.user != job_seeker_instance.user:
            return Response({'detail': 'You can only update your own profile.'}, status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)
        

    def destroy(self, request, *args, **kwargs):
        job_seeker_instance = self.get_object()

        # Ensure the authenticated user can only delete their own profile
        if request.user != job_seeker_instance.user:
            return Response({'detail': 'You can only delete your own profile.'}, status=status.HTTP_403_FORBIDDEN)
        
        # Optionally, delete the associated User instance as well
        job_seeker_instance.user.delete()
        return super().destroy(request, *args, **kwargs)  


# class DeleteUserView(generics.DestroyAPIView):
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         return self.request.user

#     def delete(self, request, *args, **kwargs):
#         user = self.get_object()

#         # Check if the provided password is correct
#         password = request.data.get('password')
#         if not user.check_password(password):
#             return Response({'detail': 'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)

#         # Delete the user account
#         self.perform_destroy(user)
#         return Response({'detail': 'Account deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
