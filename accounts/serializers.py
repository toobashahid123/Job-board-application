from rest_framework import serializers
from .models import *

class AllUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        exclude = ['password','groups','user_permissions']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'username', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            role=role  # Assign role to user
        )
        user.set_password(validated_data['password'])
        user.save()
        # Create associated Employer or JobSeeker based on role
        if role == 'employer':
            Employer.objects.create(user=user)
        elif role == 'jobseeker':
            JobSeeker.objects.create(user=user)
        return user
    
class EmployerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Employer
        fields = "__all__"

        
class JobseekerSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nest UserSerializer to include user details

    class Meta:
        model = JobSeeker
        fields = '__all__'

# class JobSeekerSerializer(serializers.ModelSerializer):
#     user = UserSerializer()

#     class Meta:
#         model = JobSeeker
#         fields = ['user', 'uuid', 'name', 'email', 'gender', 'pic', 'phone_number', 'qualification', 'resume', 'portfolio']

#     def create(self, validated_data):
#         user_data = validated_data.pop('user')
#         user_serializer = UserSerializer(data=user_data)
#         if user_serializer.is_valid():
#             user = user_serializer.save()
#             jobseeker = JobSeeker.objects.create(user=user, **validated_data)
#             return jobseeker
#         else:
#             raise serializers.ValidationError(user_serializer.errors)

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)