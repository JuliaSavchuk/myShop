from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .forms import ReviewForm
from .models import Review
from main.models import Product


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if Review.objects.filter(product=product, author=request.user).exists():
        messages.error(request, "Ви вже залишили відгук на цей товар.")
        return redirect(product.get_absolute_url())

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.author = request.user
            review.save()
            messages.success(request, "Дякуємо! Ваш відгук опубліковано.")
            return redirect(product.get_absolute_url())
    else:
        form = ReviewForm()

    return render(request, 'reviews/add_review.html', {
        'form': form,
        'product': product
    })


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.author != request.user:
        raise HttpResponseForbidden("Ви не можете редагувати чужий відгук.")

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Відгук успішно оновлено.")
            return redirect(review.product.get_absolute_url())
    else:
        form = ReviewForm(instance=review)

    return render(request, 'reviews/edit_review.html', {
        'form': form,
        'review': review
    })


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.author != request.user and not request.user.is_staff:
        raise HttpResponseForbidden("Недостатньо прав для видалення.")
    product_url = review.product.get_absolute_url()
    review.delete()
    messages.success(request, "Відгук видалено.")
    return redirect(product_url)


def mark_helpful(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.helpful_count += 1
    review.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))