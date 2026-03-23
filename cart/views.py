from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from store.models import Product
from .models import Cart, CartItem


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, _ = Cart.objects.get_or_create(
            session_key=request.session.session_key
        )
    return cart


def cart_detail(request):
    cart = get_or_create_cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)

    quantity = int(request.POST.get('quantity', 1))

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity

    item.save()

    messages.success(request, f'"{product.name}" added to cart!')
    return redirect('cart:detail')


def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()

    messages.info(request, 'Item removed from cart.')
    return redirect('cart:detail')


def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)

    quantity = int(request.POST.get('quantity', 1))

    if quantity > 0:
        item.quantity = quantity
        item.save()
    else:
        item.delete()

    return redirect('cart:detail')


def clear_cart(request):
    cart = get_or_create_cart(request)
    cart.items.all().delete()

    messages.info(request, 'Cart cleared.')
    return redirect('cart:detail')