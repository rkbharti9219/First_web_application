import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flipzon.settings')
django.setup()

from store.models import Category, Product


def create_categories():
    categories = ['Electronics', 'Clothing', 'Books', 'Home & Kitchen', 'Sports']
    cat_objects = {}

    for name in categories:
        cat, _ = Category.objects.get_or_create(name=name)
        cat_objects[name] = cat
        print(f"✅ Category: {name}")

    return cat_objects


def create_products(cat_objects):
    products = [
        {'name': 'Wireless Headphones','category': 'Electronics','price': 2999,'discount_price': 1999,'stock': 50,'featured': True,'description': 'High quality wireless headphones with noise cancellation.'},
        {'name': 'Smart Watch',
            'category': 'Electronics',
            'price': 4999,
            'discount_price': 3499,
            'stock': 30,
            'featured': True,
            'description': 'Feature-packed smartwatch with health tracking.'
        },
        {
            'name': 'Running Shoes',
            'category': 'Sports',
            'price': 1999,
            'discount_price': 1499,
            'stock': 100,
            'featured': False,
            'description': 'Lightweight running shoes for everyday training.'
        },
        {
            'name': 'Django for Beginners',
            'category': 'Books',
            'price': 499,
            'discount_price': None,
            'stock': 200,
            'featured': False,
            'description': 'Learn Django web development from scratch.'
        },
        {
            'name': 'Cotton T-Shirt',
            'category': 'Clothing',
            'price': 599,
            'discount_price': 399,
            'stock': 150,
            'featured': True,
            'description': 'Comfortable everyday cotton t-shirt.'
        },
        {
            'name': 'Coffee Maker',
            'category': 'Home & Kitchen',
            'price': 3499,
            'discount_price': 2799,
            'stock': 40,
            'featured': True,
            'description': 'Brew perfect coffee every morning.'
        },
    ]

    for p in products:
        product, created = Product.objects.get_or_create(
            name=p['name'],
            defaults={
                'category': cat_objects[p['category']],
                'price': p['price'],
                'discount_price': p['discount_price'],
                'stock': p['stock'],
                'featured': p['featured'],
                'description': p['description'],
                'available': True,
            }
        )

        if created:
            print(f"✅ Created: {p['name']}")
        else:
            print(f"⏭️ Exists: {p['name']}")


def run():
    print("🚀 Seeding database...\n")
    cat_objects = create_categories()
    create_products(cat_objects)
    print("\n🎉 Done! Visit http://127.0.0.1:8000 to see your products.")


if __name__ == "__main__":
    run()