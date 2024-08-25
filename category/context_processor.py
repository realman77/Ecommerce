from asgiref.sync import sync_to_async
from django.db.models import QuerySet
from django.http import QueryDict
from django.shortcuts import render

from .models import Category

def menu_links(request):
    categories = (Category.objects.all())
    context = {
        'categories': categories,
    }
    print(context)
    return context

