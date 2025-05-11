from django.urls import path
from .views import clear_cart

from .views import profile, register, login_view, custom_logout, remove_from_cart, buy_product

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('register/', register, name='register'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('buy_product/<int:product_id>/', buy_product, name='buy_product'),
    path('clear_cart/', clear_cart, name='clear_cart'),
]
