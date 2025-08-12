# viewer/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # --- HTML Page Routes ---
    path('', views.user_search, name='home'),
    path('search/', views.user_search, name='user_search'),
    path('user/<str:user_id>/orders/', views.user_orders, name='user_orders'),
    path('order/<str:order_id>/items/', views.order_items, name='order_items'),

    # --- REST API Route ---
    # Add the new path for our API view
    path('api/user/<str:user_id>/orders/', views.user_orders_api, name='user_orders_api'),
]