from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Avg
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Product, Category, Review


def home(request):
    featured = Product.objects.filter(available=True, featured=True)[:8]
    latest = Product.objects.filter(available=True)[:8]
    categories = Category.objects.all()

    return render(request, 'store/home.html', {
        'featured': featured,
        'latest': latest,
        'categories': categories,
    })


def product_list(request):
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()

    category_slug = request.GET.get('category')
    search_query = request.GET.get('q', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort', '-created_at')

    selected_category = None

    # Filter by category
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    # Search
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Price filters
    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    # Sorting
    sort_map = {
        'price_asc': 'price',
        'price_desc': '-price',
        'name': 'name',
        '-created_at': '-created_at',
    }

    products = products.order_by(sort_map.get(sort_by, '-created_at'))

    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
        'sort_by': sort_by,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    reviews = product.reviews.all()

    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    related = Product.objects.filter(
        category=product.category,
        available=True
    ).exclude(id=product.id)[:4]

    user_review = (
        reviews.filter(user=request.user).first()
        if request.user.is_authenticated else None
    )

    return render(request, 'store/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'related': related,
        'user_review': user_review,
    })


@login_required
def add_review(request, slug):
    product = get_object_or_404(Product, slug=slug)

    if request.method == 'POST':
        Review.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={
                'rating': request.POST.get('rating'),
                'comment': request.POST.get('comment'),
            }
        )

        messages.success(request, 'Review submitted!')
        return redirect('store:product_detail', slug=slug)

    return redirect('store:product_detail', slug=slug)