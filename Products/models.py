from django.db import models
from authentication.models import User
from authentication.models import Seller,Store

class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def discounted_price(self):
        return self.price - (self.price * self.discount/100)

    def __str__(self):
        return self.name

