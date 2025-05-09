from django.forms import ModelForm
from django import forms

from user.models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'id']
        widgets = {

        }