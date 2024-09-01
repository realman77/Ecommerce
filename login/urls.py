from django.urls import path

from login.views import *


urlpatterns = [
    path("signin/", Signin.as_view(), name="signin"),
    path("register/", Register.as_view(), name='register'),
    path('signout/', Signout.as_view(), name="signout"),
]