from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


from zipcode.models import ZipCode

# Create your models here.
class Type(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.PROTECT, default=1)
    zipcode = models.ForeignKey(ZipCode, on_delete=models.PROTECT, blank=True, null=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='profile_images', blank=True, null=True)
    banner = models.ImageField(upload_to='profile_banners', blank=True, null=True)
    logo = models.ImageField(upload_to='profile_logo', blank=True, null=True)
    phone = PhoneNumberField(region='IS', null=True)

    def __str__(self):
        return f"{self.name} {self.type.name}"
