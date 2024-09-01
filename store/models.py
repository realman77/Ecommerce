from django.db import models

from category.models import Category

# Create your models here.
class Size(models.Model):
    size = models.CharField(max_length=25)

    def __str__(self):
        return self.size


class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug  = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=999999999, decimal_places=2, blank=False, null=False)
    # decimal_places = models.DecimalField()
    image = models.ImageField(blank=False, upload_to="products/%Y/%m/%d")
    stock = models.IntegerField(blank=True, null=True, default=100)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, null=False, blank=False, on_delete=models.CASCADE)
    size = models.ManyToManyField(Size, blank=False)
    color = models.ManyToManyField(Color, blank=False)
    brand = models.CharField(max_length=100, default="")
    properties = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
