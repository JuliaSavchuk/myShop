from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Category, Product


def get_filtered_products(request, category=None):
    products = Product.objects.filter(is_available=True)
    if category:
        products = products.filter(category=category)
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    current_sort = request.GET.get('sort', '-created_at')
    valid_sorts = {
        'name': 'name',
        '-name': '-name',
        'price': 'price',
        '-price': '-price',
        'new': '-created_at',
        'old': 'created_at',
    }
    sort_field = valid_sorts.get(current_sort, '-created_at')
    products = products.order_by(sort_field)
    return products, current_sort, search_query


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
    products_qs, current_sort, search_query = get_filtered_products(request, category)
    paginator = Paginator(products_qs, 6)
    page = request.GET.get('page', 1)
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


def load_more_products(request):
    offset = int(request.GET.get('offset', 6))
    limit = 6
    category_slug = request.GET.get('category_slug')
    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
    products_qs, _, _ = get_filtered_products(request, category)
    products = products_qs[offset:offset + limit]
    html = render_to_string('main/_products.html', {'products': products})
    has_more = len(products) == limit
    return JsonResponse({
        'html': html,
        'has_more': has_more,
        'new_offset': offset + limit
    })


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, is_available=True)
    return render(request, 'main/product_detail.html', {'product': product})