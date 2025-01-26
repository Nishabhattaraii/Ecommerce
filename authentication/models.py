from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email= models.EmailField(unique=True,)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]


class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)

class Store(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="seller_user")
    full_name = models.CharField(max_length= 100)
    store = models.ForeignKey(Store,on_delete=models.CASCADE)
