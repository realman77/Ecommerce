from django.contrib import admin
from django import forms
from store.models import *

# Register your models here.


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

        widgets = {
            "size": forms.CheckboxSelectMultiple,
            'color': forms.CheckboxSelectMultiple,
        }


class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ('id', "name", 'price', 'stock', 'is_available', 'category', 'created_at')
    list_display_links = ("id", "name", "price", "stock",)
    prepopulated_fields = {"slug": ('name', )}
    ordering = ("-created_at",)
    sortable_by = ("category", "created_at")
    list_filter = ('is_available',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Size)
admin.site.register(Color)