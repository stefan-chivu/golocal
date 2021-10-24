from django import forms

class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=80)
    phone = forms.CharField(max_length=20)
    address = forms.CharField(max_length=150)
    zipcode = forms.CharField(max_length=20)
    stripe_token = forms.CharField(max_length=255)