"""This is a forms file that holds forms that the user can fill."""

from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Profile
from django import forms

# Form for registering as a user.
class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "user_type", "email", "phone", "password1", "password2")

        # Adding placeholders to form to help users understand what they need to fill in.
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'John'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Doe'}),
            'email': forms.TextInput(attrs={'placeholder': 'johndoe@example.com','autocomplete': 'email'}),
            'phone': forms.TextInput(attrs={'placeholder': '02012345678','autocomplete': 'tel'}),
        }

# Form for updating information about user.
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", "phone")

# Form for updating profile picture for user.
class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_image"]

        # FileInput hidden for custom input.
        widgets = {
            "profile_image": forms.FileInput(attrs={
                "class": "hidden"
            })
        }