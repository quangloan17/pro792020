from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from bootstrap_modal_forms.forms import BSModalModelForm, BSModalForm
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from .models import *
from django.forms import ModelForm, Textarea


class KhachHangForm(BSModalModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        widgets = {
            'popular_info': Textarea(attrs={'cols': 80, 'rows': 5}),
            'private_info': Textarea(attrs={'cols': 80, 'rows': 5}),
        }
        exclude = ['',]

class FilterForm(BSModalForm):
    type = forms.ChoiceField(choices=Customer.CATEGORY)

    class Meta:
        fields = ['type', 'clear']

class CustomerModelForm(BSModalModelForm):
    create_date = forms.DateField(
        error_messages={'invalid': 'Enter a valid date in YYYY-MM-DD format.'}
    )

    class Meta:
        model = Customer
        exclude = ['create_date']


class CustomUserCreationForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


