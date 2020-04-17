from django.db import models
from django.conf import settings


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name}"

class Order(models.Model):
    is_ordered = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered_time = models.TimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return f"""{self.is_ordered} {self.user}  """

class Menu_item(models.Model):
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    topping_number = models.IntegerField();

    def __str__(self):
        return f"{self.name}  {self.category}."

class Topping(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return f"{self.name}"

class Order_item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    Menu_item = models.ForeignKey(Menu_item, on_delete=models.CASCADE)
    quantity = models.IntegerField();
    toppings = models.ManyToManyField(Topping)

    def __str__(self):
        return f"{self.Menu_item} {self.quantity} {topping.name for topping in self.toppings.all()}"
