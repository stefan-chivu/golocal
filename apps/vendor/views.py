from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
# from PIL import Image
# import requests
# from io import BytesIO
# from django.core.files.base import ContentFile


from .forms import ProductForm, RegistrationForm

# Create your views here.

from .models import Vendor

def become_vendor(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            address = form.cleaned_data['email']
            phoneNo = form.cleaned_data['phoneNo']

            vendor = Vendor.objects.create(name=user.username, created_by=user, address=address, phoneNo=phoneNo)

            return redirect('frontpage')
    else:
        form = RegistrationForm()

    return render(request, 'vendor/become_vendor.html', {'form': form})

@login_required
def vendor_admin(request):
    vendor = request.user.vendor
    products = vendor.products.all()
    # orders = vendor.orders.all()

    # for order in orders:
    #     order.vendor_ammount = 0
    #     order.vendor_paid_amount = 0
    #     order.fully_paid = True

    #     for item in order.items.all():
    #         if item.vendor == request.user.vendor:
    #             if item.vendor_paid:
    #                 order.vendor_paid_amount += item.get_total_price()
    #             else:
    #                 order.vendor_amount += item.get_total_price()
    #                 order.fully_paid = False

    return render(request, 'vendor/vendor_admin.html', {'vendor': vendor, 'products': products})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user.vendor
            product.slug = slugify(product.title)
            product.save()

            return redirect('vendor_admin')
    else:
        form = ProductForm()

    return render(request, 'vendor/add_product.html', {'form': form})

@login_required
def edit_vendor(request):
    vendor = request.user.vendor

    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        address = request.POST.get('address', '')
        phoneNo = request.POST.get('phoneNo', '')

        if name:
            vendor.created_by.email = email
            vendor.created_by.first_name = first_name
            vendor.created_by.last_name = last_name
            vendor.created_by.save()

            vendor.address = address
            vendor.name = name
            vendor.phoneNo = phoneNo
            vendor.save()

            return redirect('vendor_admin')

    return render(request, 'vendor/edit_vendor.html', {'vendor':vendor})

def vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)

    return render(request, 'vendor/vendor.html', {'vendor': vendor})