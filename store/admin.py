from django.contrib import admin
from store.models import Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name","price","stock","category","updated_date","is_available")
    prepopulated_fields = {"slug":("name",)}

admin.site.register(Product, ProductAdmin)  