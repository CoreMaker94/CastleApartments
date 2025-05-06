from django.db import models
from userprofile.models import UserProfile

# Create your models here.

class Area(models.Model):
    name = models.CharField(max_length=50)

class City(models.Model):
    name = models.CharField(max_length=100)

class ZipCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

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

