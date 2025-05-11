from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction
from django.forms import ModelForm
from django import forms

from user.models import Profile

class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    type = forms.ModelChoiceField(
        queryset=Profile._meta.get_field('type').related_model.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2','name', 'type', 'image')

    def save(self, commit=True):
        with transaction.atomic():
            user = super().save(commit=False)
            if commit:
                user.save()
                Profile.objects.create(
                    user=user,
                    name=self.cleaned_data['name'],
                    type=self.cleaned_data['type'],
                    image=self.cleaned_data.get('image')
                )


class BuyerProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'id', 'type', 'banner', 'logo', 'phone', 'zipcode']
        widgets = {} # used for setting class for the input/selection field


class SellerProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'id', 'type']