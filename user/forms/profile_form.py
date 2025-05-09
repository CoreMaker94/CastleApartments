from django.forms import ModelForm
from django import forms

from user.models import Profile

class BuyerProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'id', 'type', 'banner', 'logo', 'phone', 'zipcode']
        widgets = {} # used for setting class for the input/selection field


class SellerProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'id', 'type']