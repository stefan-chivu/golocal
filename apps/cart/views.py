from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .cart import Cart
import stripe
from django.conf import settings
from django.contrib import messages
from .forms import CheckoutForm
from apps.order.utilites import checkout

# Create your views here.
@login_required
def place_order(request):
    cart = Cart(request)
    client = request.user.vendor
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            print("\n\n\n\n\nFORM IS VALID")
            stripe.api_key = settings.STRIPE_SECRET_KEY
            stripe_token = form.cleaned_data['stripe_token']
            
            charge = stripe.Charge.create(
                amount=int(cart.get_total_cost() * 100),
                currency='RON',
                description='Plata GoLocal',
                source=stripe_token
            )

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            zipcode = form.cleaned_data['zipcode']
            
            order = checkout(request, client, first_name, last_name, email, address, zipcode, phone, cart.get_total_cost())

            cart.clear()
            
            return redirect('success')
    else:
        form = CheckoutForm()
    return render(request, 'cart/checkout.html', {'cart': cart, 'form': form, 'stripe_pub_key': settings.STRIPE_PUB_KEY})

@login_required
def cart_detail(request):
    cart = Cart(request)

    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)

    if remove_from_cart:
        cart.remove(remove_from_cart)
        return redirect('cart')

    if change_quantity:
        cart.add(change_quantity, quantity, True)
        return redirect('cart')

    return render(request, 'cart/cart.html')
    
@login_required
def success(request):
    return render(request, 'cart/success.html')