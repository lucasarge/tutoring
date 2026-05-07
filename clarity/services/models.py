from django.db import models
from users.models import CustomUser
from django.utils.crypto import get_random_string

# Create your models here.
def generate_random_code():
    return get_random_string(length=8)

class RegisterService(models.Model):
    caregiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    student_name = models.CharField()
    caregiver_note = models.TextField()
    code = models.CharField(max_length=8, default=generate_random_code, unique=True)

    def __str__(self):
        return f"{self.caregiver.first_name}'s Registering {self.student_name}"

class Service(models.Model):
    caregiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE),
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE),
    caregiver_note = models.ForeignKey(RegisterService, on_delete=models.CASCADE)
    slug = models.CharField(max_length=8, default=generate_random_code, unique=True)

    def __str__(self):
        return f"{self.student.first_name}'s Tutoring"