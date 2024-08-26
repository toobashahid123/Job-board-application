import uuid
import os

def generate_uuid(length=8):
    """
    Generate a unique UUID string of specified length.
    """
    return str(uuid.uuid4())[:length]

def get_resume_path(instance, filename):
    """
    Generate a file path for resume uploads.
    """
    return os.path.join('resume_path', f'resume_path{instance.id}', filename)

def get_profile_pictures_path(instance, filename):
    """
    Generate a file path for profile picture uploads.
    """
    return os.path.join('profile_pictures', f'profile_pictures{instance.id}', filename)

def get_company_logos_path(instance, filename):
    """
    Generate a file path for company logo uploads.
    """
    return os.path.join('company_logos', f'company_logos{instance.id}', filename)