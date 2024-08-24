from django.contrib import admin

from store.models import Product

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", 'price', 'stock', 'is_available', 'category', 'created_at')
    prepopulated_fields = {"slug": ('name', )}
    ordering = ("-created_at",)
    sortable_by = ("category", "created_at")
    list_filter = ('is_available',)

admin.site.register(Product, ProductAdmin)