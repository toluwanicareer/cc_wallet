from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers


# Create your models here.

class Cart(models.Model):
    owner=models.ForeignKey(User, on_delete=models.CASCADE)

class Store(models.Model):
    name=models.CharField(max_length=200)
    address=models.TextField()
    logo=models.ImageField(null=True)
    state=models.CharField(max_length=200)
    country=models.CharField(max_length=200)
    owner=models.OneToOneField(User, on_delete=models.CASCADE)
    status=models.BooleanField()
    category=models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    thumbnail=models.ImageField(null=True)
    name=models.CharField(max_length=200)
    price=models.CharField(max_length=200)
    store=models.ForeignKey(Store, on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField(null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    store=models.ForeignKey(Store, on_delete=models.CASCADE)
    status=models.CharField(max_length=200)
    total_cost=models.CharField(max_length=200)

class Items(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    order=models.ForeignKey(Order,null=True, on_delete=models.CASCADE)
    quantity=models.IntegerField()
    cost=models.CharField(max_length=200)



class StoreTransaction(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE)
    amount=models.CharField(max_length=200)
    from_addr=models.CharField(max_length=200)
    to_addr=models.CharField(max_length=200)
    status=models.BooleanField(default=False)
    store=models.ForeignKey(Store, on_delete=models.CASCADE)


