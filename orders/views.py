from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from cart.views import get_or_create_cart
from .models import Order, OrderItem


@login_required
def checkout(request):
    cart = get_or_create_cart(request)

    # Check if cart is empty
    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart:detail')

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            total_amount=cart.total_price,
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            pincode=request.POST.get('pincode'),
            payment_method=request.POST.get('payment_method', 'cod'),
        )

        # Create order items
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                price=item.product.final_price,
                quantity=item.quantity,
            )

            # Update product stock
            item.product.stock -= item.quantity
            item.product.save()

        # Clear cart
        cart.items.all().delete()

        messages.success(request, f'Order #{order.id} placed successfully!')
        return redirect('orders:order_detail', order_id=order.id)

    return render(request, 'orders/checkout.html', {
        'cart': cart
    })


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)

    return render(request, 'orders/order_list.html', {
        'orders': orders
    })


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(request, 'orders/order_detail.html', {
        'order': order
    })