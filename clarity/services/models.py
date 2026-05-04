from django.db import models
from users.models import CustomUser
from django.utils.crypto import get_random_string

# Create your models here.
def generate_random_code():
    return get_random_string(length=8)

class RegisterService():
    caregiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    caregiver_note = models.TextField()
    code = models.CharField(max_length=8, default=generate_random_code, unique=True)