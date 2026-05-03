from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Profile
from django import forms

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "user_type", "email", "phone", "password1", "password2")
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'John'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Doe'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Password'}),
        }

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", "phone")

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_image"]

        widgets = {
            "profile_image": forms.FileInput(attrs={
                "class": "hidden"
            })
        }