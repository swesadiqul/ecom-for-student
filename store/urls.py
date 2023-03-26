from django.urls import path
from .views import *

urlpatterns = [
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('product-list/', product_list, name='product_list'), 
    path('product-details/<int:pk>/', product_details, name='product_details'), 
    path('add-to-cart/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('cart-summary/', cart_summary, name='cart_summary'),
    path('cart-quantity-increment/<pk>/', cart_quantity_increment, name='cart_quantity_increment'),
    path('cart-quantity-decrement/<pk>/', cart_quantity_decrement, name='cart_quantity_decrement'),
    path('remove-from-cart/<pk>/', remove_from_cart, name='remove_from_cart'),
]
