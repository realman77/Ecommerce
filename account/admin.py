from django.contrib import admin

from .models import Account

# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', "username", "last_login", "date_joined", 'is_active', 'is_staff', 'is_superadmin')
    list_display_links = ("first_name", "last_name", "email",)
    ordering = ("-date_joined",)

    # filter_horizontal = ()
    # list_filter = ()
    # fieldsets = ()
    search_fields = ("first_name", "last_name", "username",)
    sortable_by = ("first_name", 'last_name', "username",)
    # list_filter = ('is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superadmin', 'is_active')


admin.site.register(Account, AccountAdmin)