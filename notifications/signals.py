from django.core.mail import send_mail
from django.conf import settings

from django.db.models.signals import post_save
from django.dispatch import receiver
from jobs.models import JobApplication
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=JobApplication)
def send_application_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        group_name = f"notifications_{instance.job.posted_by.id}"
        message = f"New application for {instance.job.title}"

        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "send_notification",
                "message": message
            }
        )

def send_welcome_email(user):
    subject = "Welcome to Our Platform"
    message = (
        f"Dear {user.username},\n\n"
        "Thank you for signing up on our platform. We are excited to have you on board!\n\n"
        "Best regards,\n"
        "ABC Company"
    )
    recipient_list = [user.email]
    
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)


def send_status_update_email(application):
    subject = f"Update on Your Application for {application.job.title}"
    message = (
        f"Dear {application.applicant.first_name},\n\n"
        f"We wanted to inform you that the status of your application for the position "
        f"{application.job.title} has been updated to '{application.get_status_display()}'.\n\n"
        "Thank you for your continued interest.\n\n"
        "Best regards,\n"
        "ABC Company"
    )
    recipient_list = [application.applicant.email]
    
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)        