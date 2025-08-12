# viewer/views.py
from django.shortcuts import render, get_object_or_404
from .models import User, Order, OrderItem


# View 1: User Search
def user_search(request):
    """
    Handles displaying a search form and showing a list of users
    that match the search query.
    """
    query = request.GET.get('q')  # Gets the search term from the URL, e.g., ?q=John
    users = None

    if query:
        # If a query is provided, search for users whose name contains the query (case-insensitive)
        users = User.objects.filter(name__icontains=query)

    # Pass the query and the found users to the template
    context = {'query': query, 'users': users}
    return render(request, 'viewer/search.html', context)


# View 2: User's Orders
def user_orders(request, user_id):
    """
    Finds a specific user and displays all of their orders.
    """
    # Get the user object, or show a 404 Not Found page if the user doesn't exist
    user = get_object_or_404(User, id=user_id)

    # Get all orders related to this user
    # We can use 'user.orders.all()' because of the 'related_name' we set in models.py
    orders = user.orders.all()

    context = {'user': user, 'orders': orders}
    return render(request, 'viewer/user_orders.html', context)


# View 3: Order's Items
def order_items(request, order_id):
    """
    Finds a specific order and displays all the items within it.
    """
    order = get_object_or_404(Order, id=order_id)

    # Get all items related to this order
    # We use 'order.items.all()' because of the 'related_name' in our OrderItem model
    items = order.items.all()

    context = {'order': order, 'items': items}
    return render(request, 'viewer/order_items.html', context)