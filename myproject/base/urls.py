from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('profile/', views.profile, name='profile'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_details, name='product_details'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart_quantity/<int:product_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/', views.cart_view, name='cart'),
    path('buy/<int:product_id>/', views.buy, name='buy'),
    path('confirm_order/<int:product_id>/', views.confirm_order, name='confirm_order'),
    path('confirm_bulk_order/', views.confirm_bulk_order, name='confirm_bulk_order'),
]
