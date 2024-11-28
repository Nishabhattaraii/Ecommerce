from django.db import models
from authentication.models import User
from authentication.models import Seller
from django.core.validators import MinValueValidator, MaxValueValidator


class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='photos/')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0.0)])
    stock = models.PositiveIntegerField()
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def discounted_price(self):
        return self.price - (self.price * self.discount/100)

    def __str__(self):
        return self.name

class Comment(models.Model):
    author =models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='comment/images/')