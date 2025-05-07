from django.db import models

# Create your models here.
class Area(models.Model):
    name = models.CharField(max_length=50)

class City(models.Model):
    name = models.CharField(max_length=100)

class ZipCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)