from django.db import models
from django.contrib.auth.models import User
from main.models import Product


class Review(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Товар"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор"
    )
    rating = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        verbose_name="Рейтинг"
    )
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    content = models.TextField(max_length=1000, verbose_name="Текст відгуку")
    advantages = models.TextField(blank=True, verbose_name="Переваги")
    disadvantages = models.TextField(blank=True, verbose_name="Недоліки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")
    is_active = models.BooleanField(default=True, verbose_name="Активний")
    helpful_count = models.IntegerField(default=0, verbose_name="Корисно")

    class Meta:
        unique_together = ['product', 'author']
        ordering = ['-created_at']
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"

    def __str__(self):
        return f"{self.author.username} → {self.product.name} ({self.rating}★)"

    def get_rating_display_stars(self):
        return '★' * self.rating + '☆' * (5 - self.rating)