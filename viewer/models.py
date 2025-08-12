# viewer/models.py
from django.db import models

# User model remains the same
class User(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.name

# Order model remains the same
class Order(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    orderDate = models.DateTimeField()
    # Note: totalAmount is not in your orders.csv, so we remove it.
    # We can calculate it later if needed.

    def __str__(self):
        return f"Order {self.id} for {self.user.name}"

# NEW: Product model based on products.csv
class Product(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=255)
    # Add other fields from products.csv if you want, e.g., category, price
    # For now, name is enough for the viewer.

    def __str__(self):
        return self.name

# MODIFIED: This replaces the old Item model. It is based on order_items.csv
class OrderItem(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2) # price per unit at time of sale

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for Order {self.order.id}"