from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Menu_item)
admin.site.register(Category)
admin.site.register(Topping)
admin.site.register(Order)
admin.site.register(OrderStatus)
admin.site.register(Order_item)
