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
    slug = models.SlugField(max_length=100, unique=True)
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


class VariationManager(models.Manager):
    def all_types(self):
        manager = super(VariationManager, self)
        types = [i[0] for i in manager.values_list("category").distinct()]

        res = {}

        for cat_name in types:
            res[cat_name] = manager.filter(category=cat_name, is_active=True)
        return res


CATEGORY_CHOICES = (
    ("Color", "Color"),
    ("Size", "Size"),
    ('Material', 'Material')
)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    value = models.CharField(max_length=100,)
    count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self) -> str:
        return f'{self.product.name} {self.category} {self.value}'
