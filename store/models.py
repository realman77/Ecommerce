from django.db import models

from category.models import Category

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    slug  = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=999999999, decimal_places=2, blank=False, null=False)
    # decimal_places = models.DecimalField()
    image = models.ImageField(blank=True, upload_to="products/%Y/%m/%d")
    stock = models.IntegerField(blank=True, null=True, default=100)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, null=False, blank=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    