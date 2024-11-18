from django.db import models
from authentication.models import User
from Products.models import Product

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart_user")
    created_at = models.DateTimeField(auto_now_add=True)



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def item_price(self):
        """Get the discounted price of the product"""
        return self.quantity * self.product.discounted_price()

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

  
class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.discounted_price


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_amount(self):
        return sum(item.total_price() for item in self.order_items.all())

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


    
   
        
# class TimeStampModel(models.Model):
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     class Meta:
#         abstract = True
        
# class Cart(TimeStampModel):
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE
#     )
#     product = models.ForeignKey(
#         Product, on_delete=models.CASCADE
#     )
#     quantity = models.PositiveIntegerField(default=1)