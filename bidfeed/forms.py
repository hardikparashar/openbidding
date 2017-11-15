from django import forms
from django.contrib.auth.models import User

from .models import Product, Bid


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['product_name', 'start_price', 'min_increase', 'product_image','days','description']


class BidForm(forms.ModelForm):

    class Meta:
        model = Bid
        fields = ['bid_value']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
