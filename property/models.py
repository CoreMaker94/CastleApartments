from django.db import models
from userprofile.models import UserProfile
from zipcode.models import ZipCode

# Create your models here.

class Type(models.Model):
    name = models.CharField(max_length=50)

class Property(models.Model):
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    zipcode = models.ForeignKey(ZipCode, on_delete=models.CASCADE)
    address = models.CharField(max_length=50) # is 100 too much or too little
    rooms = models.IntegerField()
    beds = models.IntegerField()
    bath = models.IntegerField()
    size = models.IntegerField()
    description = models.TextField()
    price = models.IntegerField()
    list_date = models.DateField()

