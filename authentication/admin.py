from django.contrib import admin

# Register your models here.
from authentication.models import Customer, Seller, Store

admin.site.register(Customer),
admin.site.register(Seller),
admin.site.register(Store),
