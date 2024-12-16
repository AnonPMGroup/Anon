from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    CATEGORY_TYPE_CHOICES = [
        ('M', 'Мужская'),
        ('F', 'Женская'),
    ]

    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    category_type = models.CharField(
        max_length=1,
        choices=CATEGORY_TYPE_CHOICES,
        default='M'
    )
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название продукта")
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name="products", 
        verbose_name="Категория"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание продукта")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    stock = models.PositiveIntegerField(verbose_name="Количество на складе")
    available = models.BooleanField(default=True, verbose_name="Доступен для заказа")
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name"]

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.user.username}'s cart"

    def total_price(self):
        return self.product.price * self.quantity

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="favorited_by")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product') 
        ordering = ['-added_at']  

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    