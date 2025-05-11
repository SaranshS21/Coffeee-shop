from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Product
from django.db.models import Q


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def services(request):
    return render(request, 'services.html')


def contact(request):
    return render(request, 'contact.html')


def product_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        products = Product.objects.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )
    else:
        products = Product.objects.all()
    return render(request, 'products.html', {'products': products, 'search_query': search_query})


@login_required
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, pk=product_id)
    product_id_str = str(product.id)

    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    else:
        cart[product_id_str] = {
            'product_id': product.id,
            'name': product.name,
            'price': float(product.price),
            'quantity': 1
        }

    request.session['cart'] = cart
    return redirect('cart')


@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('cart')


@login_required
def update_cart_quantity(request, product_id):
    if request.method == "POST":
        action = request.POST.get("action")
        cart = request.session.get('cart', {})
        product_id_str = str(product_id)
        if product_id_str in cart:
            if action == "increase":
                cart[product_id_str]['quantity'] += 1
            elif action == "decrease" and cart[product_id_str]['quantity'] > 1:
                cart[product_id_str]['quantity'] -= 1
        request.session['cart'] = cart
    return redirect('cart')


@login_required
def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for item in cart.values():
        try:
            product = get_object_or_404(Product, pk=item['product_id'])
            quantity = item['quantity']
            price = item['price']
            subtotal = quantity * price
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'price': price,
                'subtotal': subtotal
            })
            total += subtotal
        except:
            continue

    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})


@login_required
def buy(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = request.session.get('cart', {})
    quantity = cart.get(str(product.id), {}).get('quantity', 1)
    return render(request, 'buy.html', {'product': product, 'quantity': quantity})


@login_required
def confirm_order(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        payment_method = request.POST.get("payment_method")
        quantity = int(request.POST.get("quantity", 1))
        total = quantity * product.price

        cart = request.session.get('cart', {})
        cart[str(product.id)] = {
            'name': product.name,
            'price': float(product.price),
            'quantity': quantity,
            'product_id': product.id
        }
        request.session['cart'] = cart

        context = {
            "product": product,
            "name": name,
            "address": address,
            "phone": phone,
            "payment_method": payment_method,
            "quantity": quantity,
            "total": total,
        }
        return render(request, "confirm_order.html", context)
    return redirect("product_list")


@login_required
def buy_all(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')

    products = []
    total = 0
    for item in cart.values():
        product = get_object_or_404(Product, pk=item['product_id'])
        quantity = item.get('quantity', 1)
        subtotal = product.price * quantity
        products.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
        total += subtotal

    return render(request, 'buy_all.html', {'products': products, 'total': total})


@login_required
@require_POST
def confirm_bulk_order(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')

    name = request.POST.get("name")
    address = request.POST.get("address")
    phone = request.POST.get("phone")
    payment_method = request.POST.get("payment_method")

    products = []
    total = 0
    for item in cart.values():
        product = get_object_or_404(Product, pk=item['product_id'])
        quantity = item.get('quantity', 1)
        subtotal = product.price * quantity
        products.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
        total += subtotal

    request.session['cart'] = {}

    return render(request, 'confirm_order.html', {
        'products': products,
        'name': name,
        'address': address,
        'phone': phone,
        'payment_method': payment_method,
        'total': total,
    })

@login_required
def profile(request):
    cart = request.session.get('cart', {})
    cart_products = []

    for item in cart.values():
        try:
            product = get_object_or_404(Product, pk=item['product_id'])
            cart_products.append({
                'id':       product.id,
                'name':     product.name,
                'price':    product.price,
                'quantity': item['quantity'],
                'subtotal': product.price * item['quantity'],
            })
        except Product.DoesNotExist:
            continue

    return render(request, 'profile.html', {
        'cart_products': cart_products,
        'search_query':  request.GET.get('search', ''),
    })

def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    all_products = Product.objects.exclude(id=product_id)

    context = {
        'product': product,
        'products': all_products,
    }
    return render(request, 'product_details.html', context)