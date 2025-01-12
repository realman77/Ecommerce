from os import name
from django.db import models

from store.models import Product, Variation

# Create your models here.
class Cart(models.Model):
    data_added = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=200, default='') 

    # def __str__(self):
    #     return self.name

class CartItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)   
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    variations = models.ManyToManyField(Variation, blank=True)
    def __str__(self):
        return self.product.name
    
    def get_total(self):
        return self.quantity * self.product.price