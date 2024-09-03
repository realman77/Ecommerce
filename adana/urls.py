"""
URL configuration for adana project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from adana.views import ProductsView


urlpatterns = ([
    path('admin/', admin.site.urls),
    path("", ProductsView.as_view(), name="home"),
    # path("", include("adana_app.urls")),
    # path("categories/", include("category.urls")),
    path('store/', include('store.urls')),
    path("cart/", include("cart.urls")),
    path('', include('login.urls')),
    path('place_order/', include('place_order.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
