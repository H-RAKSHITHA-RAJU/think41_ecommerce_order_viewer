from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.user_search, name='user_search'),
    path('user/<str:user_id>/orders/', views.user_orders, name='user_orders'),
    path('order/<str:order_id>/items/', views.order_items, name='order_items'), # <-- Check for commas
]