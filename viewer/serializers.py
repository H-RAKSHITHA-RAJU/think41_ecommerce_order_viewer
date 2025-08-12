# viewer/serializers.py
from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    # We add a custom field that is not on the model directly
    # It's a read-only field that we will calculate in our view.
    total_amount = serializers.FloatField(read_only=True)

    class Meta:
        model = Order
        # List the fields you want to include in the JSON output
        fields = ['id', 'user', 'orderDate', 'total_amount']