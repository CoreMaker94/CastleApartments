from django.contrib.auth.models import User
from django.db import models
from django.db.models import UniqueConstraint, Q

from zipcode.models import ZipCode

# Create your models here.

class Type(models.Model):
    name = models.CharField(max_length=50)

class Property(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    zipcode = models.ForeignKey(ZipCode, on_delete=models.CASCADE)
    address = models.CharField(max_length=50) # Probably 50 is enough for max_length
    rooms = models.IntegerField()
    beds = models.IntegerField()
    bath = models.IntegerField()
    size = models.DecimalField(max_digits=6, decimal_places=1) # Largest buildings are around XX.XXX,X sqrm
    description = models.TextField()
    price = models.IntegerField()
    list_date = models.DateField()
    is_sold = models.BooleanField(default=False, null=False)

    def main_image(self):
        return self.images.filter(is_main=True).first() or self.images.first()

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images', blank=True, null=True)
    is_main = models.BooleanField(default=False)

    class Meta:
        constraints = [
            #Ensures only one main image
            UniqueConstraint(
                fields=['property'],
                condition=Q(is_main=True),
                name='only_one_main_image_per_property'
            )
        ]
