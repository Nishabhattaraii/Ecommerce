from django.contrib import admin
from Products.models import Product
from authentication.models import User, Seller
# Register your models here.

admin.site.register(Product)
admin.site.register(User)
admin.site.register(Seller)