from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone, first_name, last_name, password=None, **extra_fields):
        if not email: raise ValueError("Must provide your email address.")
        if not phone: raise ValueError("Must provide your phone number.")
        if not first_name or not last_name:
            raise ValueError("Must provide your first and last name.")
        
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
    
    def create_superuser(self, email, phone, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

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

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)

    # Overriding default blank=True
    first_name = models.CharField(max_length=15, blank=False, null=False)
    last_name = models.CharField(max_length=15, blank=False, null=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone", "first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"