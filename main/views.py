from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from .models import Category, Product


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True)  # ← виправлено

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # Пошук
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )

    # Сортування
    current_sort = request.GET.get('sort', '-created_at')  # також виправлено на created_at, якщо у вас created_at
    valid_sorts = {
        'name': 'name',
        '-name': '-name',
        'price': 'price',
        '-price': '-price',
        'new': '-created_at',
        'old': 'created_at',
    }
    if current_sort in valid_sorts:
        products = products.order_by(valid_sorts[current_sort])
    else:
        current_sort = '-created_at'
        products = products.order_by('-created_at')

    # Пагінація — 6 товарів на сторінку
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)

    context = {
        'category': category,
        'categories': categories,
        'products': products_page,
        'current_sort': current_sort,
        'search_query': search_query,
    }
    return render(request, 'main/product_list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, is_available=True)
    return render(request, 'main/product_detail.html', {'product': product})