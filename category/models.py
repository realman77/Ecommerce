from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="photo/category/" ,blank=True)
    slug = models.SlugField(max_length=50,unique=True)

    def __str__(self):
        return self.name
    
    def get_url(self):
        return reverse("products_by_category", args=[self.slug])