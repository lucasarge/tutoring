"""This file defines database models and their fields."""

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator, EmailValidator

# Because I changed AbstractUser the BaseUserManager would crash. This accounts for the changes.
class CustomUserManager(BaseUserManager):

    # Used to create an average user.
    def create_user(self, email, phone, first_name, last_name, password=None, **extra_fields):

        # Ensures that user form has the required fields.
        if not email: raise ValueError("Must provide your email address.")
        if not phone: raise ValueError("Must provide your phone number.")
        if not first_name or not last_name:
            raise ValueError("Must provide your first and last name.")

        # Adjusts the users inputted email to remove weird capitalisation for example before saving it.
        email = self.normalize_email(email)
        user = self.model(
            email = email,
            phone = phone,
            first_name = first_name,
            last_name = last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Used to create superuser that can access the admin dashboard.
    def create_superuser(self, email, phone, first_name, last_name, password=None, **extra_fields):

        # Sets fields required to access admin dashboard to true.
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Confirms that the user is staff and superuser.
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(
            email=email,
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            password=password,
            **extra_fields
        )

# A custom model for storing users, customised from Djangos default.
class CustomUser(AbstractUser):

    # Username set to none as it is not used from AbstractUser, adds customfields that are required.
    username=None
    first_name = models.CharField(max_length=15, blank=False, null=False)
    last_name = models.CharField(max_length=15, blank=False, null=False)

    # Constant list with tuples of different user type choices and their field.
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('caregiver', 'Caregiver'),
        ('tutor', 'Tutor')
    ]
    user_type = models.CharField(choices=USER_TYPE_CHOICES)

    # Adds restrictions to EmailField with Djangos validator used and an error message.
    email=models.EmailField(
          max_length=254,
          unique=True,
          validators=[EmailValidator(message="Please enter a valid email address.")]
          )

    # Adds restrictions to CharField with Djangos validator used and an error message.
    phone=models.CharField(
          max_length=15, 
          unique=True,
          validators=[RegexValidator(r'^\d+$', "Please enter a valid phone number.")]
          )

    # Sets username field to be replaced with email. Editing Django's authenticator. Sets required fields.
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone", "first_name", "last_name", "user_type"]

    # Attaches custom creation logic to this model. Returns first and last name in admin dashboard.
    objects = CustomUserManager()
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Profile model with a file upload that goes to 'profile_images' and stores description for tutor.
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images', default='profile_images/default.png')
    description = models.TextField(null=True, blank=False)
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"