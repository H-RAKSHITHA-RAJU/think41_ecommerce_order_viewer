import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from viewer.models import User, Order, Product, OrderItem

class Command(BaseCommand):
    help = 'Loads data from the correct CSV files into the database'

    def handle(self, *args, **kwargs):
        # Clear existing data in the correct order (children first)
        self.stdout.write("Clearing old data...")
        OrderItem.objects.all().delete()
        Product.objects.all().delete()
        Order.objects.all().delete()
        User.objects.all().delete()

        dataset_path = os.path.join(settings.BASE_DIR, 'ecommerce_dataset')

        # --- Load Users --- (Your fix was already correct)
        self.stdout.write("Loading users...")
        with open(os.path.join(dataset_path, 'users.csv'), newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                full_name = f"{row['first_name']} {row['last_name']}"
                User.objects.create(id=row['id'], name=full_name, email=row['email'])
        self.stdout.write(self.style.SUCCESS('Successfully loaded users'))

        # --- Load Orders --- (Using 'order_id' from your head command)
        self.stdout.write("Loading orders...")
        with open(os.path.join(dataset_path, 'orders.csv'), newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # We need to handle cases where a user might not exist in our DB yet
                try:
                    user_instance = User.objects.get(id=row['user_id'])
                    Order.objects.create(
                        id=row['order_id'],  # FIX: Use 'order_id'
                        user=user_instance,
                        orderDate=row['created_at'],
                    )
                except User.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Skipping order {row['order_id']} because user {row['user_id']} does not exist."))
        self.stdout.write(self.style.SUCCESS('Successfully loaded orders'))

        # --- Load Products --- (Your head command shows 'id' and 'name' are correct)
        self.stdout.write("Loading products...")
        with open(os.path.join(dataset_path, 'products.csv'), newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Product.objects.create(id=row['id'], name=row['name'])
        self.stdout.write(self.style.SUCCESS('Successfully loaded products'))

        # --- Load Order Items --- (Using 'id', 'order_id', 'product_id', and 'sale_price' from your head command)
        self.stdout.write("Loading order items...")
        with open(os.path.join(dataset_path, 'order_items.csv'), newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    order_instance = Order.objects.get(id=row['order_id'])
                    product_instance = Product.objects.get(id=row['product_id'])
                    OrderItem.objects.create(
                        id=row['id'],            # FIX: 'id' is correct for this file
                        order=order_instance,
                        product=product_instance,
                        # ASSUMPTION: The file has no 'quantity'. We assume each row is for a quantity of 1.
                        quantity=1,
                        price=row['sale_price']  # FIX: Use 'sale_price'
                    )
                except Order.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Skipping order item {row['id']} because order {row['order_id']} does not exist."))
                except Product.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Skipping order item {row['id']} because product {row['product_id']} does not exist."))
        self.stdout.write(self.style.SUCCESS('Successfully loaded order items'))