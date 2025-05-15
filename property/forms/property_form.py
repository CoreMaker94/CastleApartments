from django import forms
from property.models import Property, PropertyImage

class CreatePropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ["seller", "property", "is_sold", "list_date"]

class PropertyImageForm(forms.ModelForm):
    main_image = forms.ImageField(
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
    )
    other_images = forms.FileField(widget=forms.TextInput(attrs={
        "multiple": True,
        'class': "form-control",
        'type': 'file',
    }),
        required=False
    )
    class Meta:
        model = PropertyImage
        exclude = ["property", "image", 'is_main']
