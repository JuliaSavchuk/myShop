from django.db import models
from django.urls import reverse
from django.utils.html import format_html


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Назва")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Опис")
    image = models.ImageField(upload_to="categories/", blank=True, null=True, verbose_name="Зображення")
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        ordering = ['name']
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main:product_list_by_category', kwargs={'category_slug': self.slug})


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Категорія",
        null=True,   
        blank=True  
    )
    name = models.CharField(max_length=200, verbose_name="Назва")
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="Slug",
        null=True,   
        blank=True   
    )
    description = models.TextField(verbose_name="Опис")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Ціна зі знижкою")
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True, null=True, verbose_name="Зображення")
    views = models.PositiveIntegerField(default=0, verbose_name="Перегляди")
    featured = models.BooleanField(default=False, verbose_name="Рекомендований")
    is_available = models.BooleanField(default=True, verbose_name="В наявності")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main:product_detail', kwargs={'id': self.id, 'slug': self.slug})