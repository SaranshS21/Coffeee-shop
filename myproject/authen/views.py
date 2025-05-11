from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from base.models import Product


def login_view(request):
    """Handle user login."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    return render(request, 'login.html')


@login_required
def profile(request):
    """View for logged-in users with cart display."""
    cart = request.session.get('cart', {})

    # Fix: Convert cart to dict if it's incorrectly a list
    if isinstance(cart, list):
        cart = {}
        request.session['cart'] = cart

    cart_products = []

    for item in cart.values():
        product_id = item.get('id')
        if not product_id:
            continue

        cart_products.append({
            'id': product_id,
            'name': item.get('name', 'Unnamed Product'),
            'price': item.get('price', 0),
            'quantity': item.get('quantity', 1),
        })

    return render(request, 'profile.html', {'cart_products': cart_products})


def register(request):
    """Handle user registration."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully!')
            login(request, user)
            return redirect('profile')
        else:
            for error in form.errors.values():
                messages.error(request, error)
            print(form.errors)
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


def custom_logout(request):
    """Handle user logout."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('profile')


@require_POST
@login_required
def remove_from_cart(request, product_id):
    """Remove a product from the cart."""
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    messages.success(request, "Item removed from cart.")
    return redirect('profile')


@require_POST
@login_required
def buy_product(request, product_id):
    """Buy a product and remove it from the cart."""
    cart = request.session.get('cart', {})
    item = cart.pop(str(product_id), None)
    request.session['cart'] = cart

    if item:
        messages.success(request, f"You bought {item['name']} successfully!")
    else:
        messages.error(request, "Product not found in cart.")
    
    return redirect('profile')


# Optional utility view to reset the cart if needed
@login_required
def clear_cart(request):
    request.session['cart'] = {}
    return HttpResponse("Cart has been cleared.")
