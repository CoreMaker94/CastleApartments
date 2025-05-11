from django.forms import ModelForm
from purchaseoffer.models import Offer
from django import forms


class PurchaseOfferForm(ModelForm):
    offer = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    expires_at = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Offer
        exclude = ['buyer', 'property', 'status', 'created_at']