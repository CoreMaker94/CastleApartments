from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey
# from encrypted_model_fields.fields import EncryptedCharField

from property.models import Property, ZipCode

# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class PaymentMethod(models.Model):
    name = models.CharField(max_length=15)

class Offer(models.Model):
    property = ForeignKey(Property, on_delete=models.PROTECT) # Unsure how to handle deletion of property
    buyer = ForeignKey(User, on_delete=models.PROTECT)
    status = ForeignKey(Status, on_delete=models.PROTECT)
    offer = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
    expires_at = models.DateField()
    # Logical things to check
    # buyer != property.seller

    def __str__(self):
        return f"{self.property.address} {self.buyer} {self.offer}"

class Finalize(models.Model):
    # If using encrypted field remember to uncomment ENCRYPTED_MODEL_FIELDS_KEY in settings.py
    offer = ForeignKey(Offer, on_delete=models.PROTECT)
    buyer_address = models.CharField(max_length=50)
    buyer_zipcode = models.CharField(max_length=20) # probably shouldn't reference zipcode table
    buyer_country = models.CharField(max_length=20)
    buyer_city = models.CharField(max_length=50)
    pay_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)



