# api/models.py
from django.db import models
from django.contrib.auth.models import User



class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    stock = models.IntegerField()

    def __str__(self):
        return self.name

class Order(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=0, default=0)  # Campo para el precio total

    def __str__(self):
        return f'Order {self.id} by {self.user.username}'

class ProductsOrders(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return f'{self.quantity} of {self.product.name} in Order {self.order.id}'