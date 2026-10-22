from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *


# Custom select widget to disable the placeholder option
class DisabledPlaceholderSelect(forms.Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value == "":
            option["attrs"]["disabled"] = True
        return option

# Registration form
class RegistrationForm(UserCreationForm):
    GENDER_CHOICES = [
        ("", "Select your gender"),
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    email = forms.EmailField(required= True)
    phone = forms.CharField(max_length=15, required=True)
    age = forms.IntegerField(required=True)
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        required=True,
        initial="",
        widget=DisabledPlaceholderSelect,
    )
    profile_image = forms.ImageField(required=True)
    
    class Meta:
        model=User
        fields = [
            "first_name",
            "last_name",
            "username",
            "age",
            "gender",
            "email",
            "phone",
            "profile_image",
            "password1",
            "password2",
        ]
        

