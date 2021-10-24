from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from phonenumber_field.formfields import PhoneNumberField

from apps.product.models import Product
from apps.vendor.models import Vendor

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'image', 'title', 'description', 'price']

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email', error_messages={'exists': 'An account with this email already exists'})
    first_name = forms.CharField(max_length=30, required=False, label='Prenume')
    last_name = forms.CharField(max_length=30, required=False, label='Nume')
    phoneNo = PhoneNumberField()
    address = forms. CharField(max_length=150, required=False, label='Adresa')

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "phoneNo", "address", "password1", "password2")

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise ValidationError(self.fields['email'].error_messages['exists'])
        return self.cleaned_data['email']