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
    service = models.OneToOneField("Service", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.caregiver.first_name}"
    
    
class Document(models.Model):
    title = models.CharField()
    file = models.FileField(upload_to='documents')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Service(models.Model):

    YEAR_CHOICES = [
        (7, "7"),
        (8, "8"),
        (9, "9"),
        (10, "10"),
        (11, "11")
    ]

    caregiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="service_caregiver")
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="service_student")
    tutor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="service_tutor", limit_choices_to={'user_type': 'tutor'}, blank=True, null=True)
    
    caregiver_note = models.TextField(blank=True)
    student_note = models.TextField(blank=True)

    year = models.IntegerField(choices=YEAR_CHOICES, blank=True, null=True)
    subjects = models.ManyToManyField('Subject', through='SubjectService')

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.student.first_name

class Resource(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    tutor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="resource_tutor")
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    message = models.TextField()
    opened = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document.title} for {self.service.student.first_name}"

class Subject(models.Model):
    name = models.CharField()
    description = models.TextField()

    def __str__(self):
        return self.name

class SubjectService(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return self.service.student.first_name

class Session(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    note = models.CharField(null=True, blank=True)
    start = models.DateTimeField()
    link = models.CharField(null=True, blank=True)

    DURATION_CHOICES = [
        (30, '30 Minutes'),
        (45, '45 Minutes'),
        (60, '60 Minutes'),
        (75, '75 Minutes'),
        (90, '90 Minutes'),
    ]

    duration = models.IntegerField(choices=DURATION_CHOICES)
    end = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.service.student.first_name}'s Tutoring Session"
    