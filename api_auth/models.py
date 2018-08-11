from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Wallet(models.Model):
    address=models.CharField(max_length=200)
    user=models.OneToOneField(User, on_delete=models.CASCADE)

class Transaction(models.Model):
    from_addr=models.CharField(max_length=200)
    to_addr=models.CharField(max_length=200)
    amount_in_wei=models.CharField(max_length=200)
    mined_status=models.BooleanField(default=False)
    tx_hash=models.CharField(max_length=200)
    currency=models.CharField(max_length=100, default='eth')
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
