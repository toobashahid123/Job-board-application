from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Job, JobApplication
from .serializers import *
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from notifications.signals import send_status_update_email


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'company', 'location']

    def create(self, request, *args, **kwargs):
        if request.user.role != 'employer':
            return Response({'detail': 'Only Employer can create job posts.'}, status=status.HTTP_403_FORBIDDEN)
        
        response = super().create(request, *args, **kwargs)
        
        # Notify clients about the new job post
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notifications",
            {
                "type": "send_notification",
                "message": f"New job posted: {response.data['title']}"
            }
        )
        
        return response
    
    def perform_create(self, serializer):
        # Set the `posted_by` field to the currently authenticated user
        serializer.save(posted_by=self.request.user)
    


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.role != 'employer' or instance.posted_by != request.user:
            return Response({'detail': 'You are not allowed to update this job post.'}, status=status.HTTP_403_FORBIDDEN)
        
        response = super().update(request, *args, **kwargs)
        
        # Notify clients about the job status update
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notifications",
            {
                "type": "send_notification",
                "message": f"Job updated: {response.data['title']}"
            }
        )
        
        return response
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.role != 'employer' or instance.posted_by != request.user:
            return Response({'detail': 'You are not allowed to delete this job post.'}, status=status.HTTP_403_FORBIDDEN)
        
        response = super().destroy(request, *args, **kwargs)
        
        # Notify clients about the job deletion
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notifications",
            {
                "type": "send_notification",
                "message": f"Job deleted: {instance.title}"
            }
        )
        
        return response

class JobApplicationCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if request.user.role != 'jobseeker':
            return Response({'detail': 'Only Job Seekers can apply for jobs.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = JobApplicationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            job_application = serializer.save(applicant=request.user)
            detailed_serializer = JobApplicationDetailSerializer(job_application, context={'request': request})

            # Notify clients about the new job application
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "notifications",
                {
                    "type": "send_notification",
                    "message": f"Application has been submitted for job {job_application.job.title}!"
                }
            )
            
            return Response(detailed_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class EmployerJobApplicationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JobApplicationDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'employer':
            # Filter job applications for jobs posted by the authenticated employer
            return JobApplication.objects.filter(job__posted_by=user)
        
        return JobApplication.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    


class JobApplicationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JobApplicationDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'employer':
            return JobApplication.objects.filter(job__posted_by=self.request.user)
        elif self.request.user.role == 'jobseeker':
            return JobApplication.objects.filter(applicant=self.request.user)
        return JobApplication.objects.none()

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def update_status(self, request, pk=None):
        application = self.get_object()

        # Ensure that only the employer who posted the job can update the status
        if request.user.role != 'employer' or request.user != application.job.posted_by:
            return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = JobApplicationStatusUpdateSerializer(application, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # Send the status update email
            send_status_update_email(application)
            self.notify_applicant(application)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def notify_applicant(self, application):
        channel_layer = get_channel_layer()
        group_name = f"user_{application.applicant.id}"

        notification_data = {
            'message': f"Your application status has been updated to {application.status}.",
            'application_id': application.id
        }

        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'send_notification',
                'message': notification_data['message']
            }
        )    