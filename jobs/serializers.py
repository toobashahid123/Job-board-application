from rest_framework import serializers
from .models import Job, JobApplication

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'company', 'location','salary', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'posted_by']


class JobApplicationDetailSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)
    applicant_email = serializers.EmailField(source='applicant.email', read_only=True)
    resume = serializers.SerializerMethodField()
    
    class Meta:
        model = JobApplication
        fields = ['id', 'job', 'applicant', 'applicant_email', 'cover_letter', 'resume', 'applied_at','status']
        read_only_fields = ['id', 'job', 'applicant', 'applicant_email', 'applied_at','status']

    def get_resume(self, obj):
        if obj.resume:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.resume.url) if request else obj.resume.url
        return None    

      

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['job', 'cover_letter', 'resume']

    def validate(self, data):
        job = data['job']
        user = self.context['request'].user
        
        # Check if the job is active
        if not job.is_active:
            raise serializers.ValidationError("You cannot apply to an inactive job.")
        
        # Check if the user has already applied
        if JobApplication.objects.filter(job=job, applicant=user).exists():
            raise serializers.ValidationError("You have already applied for this job.")
        
        return data    

class JobApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['status']
        extra_kwargs = {
            'status': {'required': True}
        }