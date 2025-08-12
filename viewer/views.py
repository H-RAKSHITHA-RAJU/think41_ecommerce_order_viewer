# viewer/views.py
from django.shortcuts import render, get_object_or_404
from .models import User, Order, OrderItem
from django.db.models import Sum  # Import Sum


# View 1: User Search
def user_search(request):
    query = request.GET.get('q')
    users = None

    if query:
        # Sort results by name
        users = User.objects.filter(name__icontains=query).order_by('name')

    context = {'query': query, 'users': users}
    return render(request, 'viewer/search.html', context)


# View 2: User's Orders
def user_orders(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Get all orders and sort by date, newest first (descending)
    orders = user.orders.all().order_by('-orderDate')

    # Calculate the total for each order
    for order in orders:
        # For each order, find the sum of the 'price' of all its related OrderItems
        # The result is stored in a new dictionary key 'total'
        order_total = order.items.aggregate(total=Sum('price'))
        order.total_amount = order_total['total'] or 0  # Use 'or 0' in case an order has no items

    context = {'user': user, 'orders': orders}
    return render(request, 'viewer/user_orders.html', context)


# View 3: Order's Items (no changes needed here)
def order_items(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = order.items.all()
    context = {'order': order, 'items': items}
    return render(request, 'viewer/order_items.html', context)
# viewer/views.py

# ... (keep all your existing imports and views) ...

# Add new imports for DRF
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import OrderSerializer


# --- API VIEW ---

@api_view(['GET']) # This decorator specifies this view only accepts GET requests
def user_orders_api(request, user_id):
    """
    This is a REST API endpoint that returns all orders for a user as JSON.
    """
    # 1. Fetch the data (same logic as before)
    user = get_object_or_404(User, id=user_id)
    orders = user.orders.all().order_by('-orderDate')

    # 2. Calculate the total for each order (same logic as before)
    for order in orders:
        order_total = order.items.aggregate(total=Sum('price'))
        order.total_amount = order_total['total'] or 0

    # 3. Serialize the data (the "translation" step)
    # We pass the queryset of orders to our serializer. 'many=True' is needed
    # because we are serializing a list of objects.
    serializer = OrderSerializer(orders, many=True)

    # 4. Return the JSON response
    return Response(serializer.data)