from django.db import models
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-price']
        indexes = [
            models.Index(fields=['category', '-price']),
            models.Index(fields=['-price']),
            models.Index(fields=['id'])
        ]

    def __str__(self):
        return f"{self.name} (${self.price})"