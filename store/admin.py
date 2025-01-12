from django.contrib import admin
from store.models import Product, Variation

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name","price","stock","category","updated_date","is_available")
    prepopulated_fields = {"slug":("name",)}

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'category', 'value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product','category')
admin.site.register(Product, ProductAdmin)  


admin.site.register(Variation, VariationAdmin)