from django.db import models
from users.models import CustomUser
from django.utils.crypto import get_random_string

# Create your models here.
def generate_code():
    return get_random_string(length=8)

class Invite(models.Model):
    
    caregiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="created_invite") 
    code = models.CharField(max_length=8, unique=True, editable=False)
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"{self.caregiver.first_name}"

class Service(models.Model):

    caregiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="service_caregiver")
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="service_student")
    
    def __str__(self):
        return f"{self.student.first_name}"