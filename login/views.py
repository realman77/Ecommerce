from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.template.response import TemplateResponse

from asgiref.sync import sync_to_async

from login.forms import RegistrationForm

from django.contrib.auth import aauthenticate, alogin
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

# Create your views here.
# class Signin(View):

class Signin(View):
    async def get(self, request):
        form = AuthenticationForm()
        return TemplateResponse(request, 'signin.html', {'form': form})

    async def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if await sync_to_async(form.is_valid)():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(username)
            print(password)
            user = await aauthenticate(username=username, password=password)
            if user is not None:
                await alogin(request, user)
                messages.success(request, f'Welcome back, {user.email}!')
                return redirect('home')  # Replace 'home' with your desired redirect URL
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
        
        return TemplateResponse(request, 'signin.html', {'form': form})


class Register(View):
    async def get(self, request):
        form = RegistrationForm()
        context = {
            'form': form,
        }
        return TemplateResponse(request, "register.html", context)

    async def post(self, request):
        form = RegistrationForm(request.POST)
        if await sync_to_async(form.is_valid)():
            print("Valid--------------------------------")
            await sync_to_async(form.save)()
            return redirect("signin")

        context = {
            'form': form,
        }
        print("Not valid***************************************")
        print(form.errors)
        return TemplateResponse(request, "register.html", context)


class Signout(View):
    async def get(self, request):
        await auth.alogout(request)
        return redirect("signin")