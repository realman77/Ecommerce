from django.contrib.auth.forms import UserCreationForm
from django import forms

from account.models import Account, City, Country


class RegistrationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('first_name', "last_name", "username", 'email', "gender", "city", "country")
    
        widgets = {
            'gender': forms.RadioSelect,
            'city': forms.Select,
            "counrty": forms.Select,
        }

    gender = forms.ChoiceField(
        choices=[('1', 'Male'), ('0', 'Female')],
        widget=forms.RadioSelect,
        required=False, # Make gender optional if needed
        label=''
    )

    # GENDER_CHOICES = [
    #     ('male', 'Male'),
    #     ('female', 'Female'),
    #     ('other', 'Other'),
    # ]
    # gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)

    # city = forms.ModelMultipleChoiceField(
    #     queryset=City.objects.all(),
    #     widget=forms.Select,
    #     required=False,
    #     label=""
    # )

    city = forms.ModelChoiceField(queryset=City.objects.all(), empty_label="Choose...")
    country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label="Choose...")
