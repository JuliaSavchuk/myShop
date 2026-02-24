from django.db import models
from django.contrib.auth.models import User
from main.models import Product

class CartItem(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart_items',
        verbose_name="Користувач"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Кількість")

    class Meta:
        unique_together = ('user', 'product')
        verbose_name = "Елемент корзини"
        verbose_name_plural = "Елементи корзини"

    def __str__(self):
        return f"{self.product.name} ({self.quantity} шт.) для {self.user.username}"