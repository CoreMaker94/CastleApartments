from django.db import models

from zipcode.models import ZipCode

class Type(models.Model):
    name = models.CharField(max_length=50)

# Create your models here.
class UserProfile(models.Model):
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    zipcode = models.ForeignKey(ZipCode, on_delete=models.PROTECT, blank=True, null=True)
    name = models.CharField(255)
    address = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='profile_images', blank=True, null=True)
    banner = models.ImageField(upload_to='profile_banners', blank=True, null=True)
    logo = models.ImageField(upload_to='profile_logo', blank=True, null=True)
    phone = models.CharField(blank=True, null=True, max_length=20)