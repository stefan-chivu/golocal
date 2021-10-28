from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.admin.views.decorators import staff_member_required
from slugify import slugify

from apps.moderator.forms import AddCategoryForm

from apps.product.models import Category, Product
from apps.vendor.models import Vendor

@staff_member_required
def delete_category(request, category_id=None):
    object = Category.objects.get(id=category_id)
    object.delete()
    return redirect('manage_categories')

@staff_member_required
def delete_product(request, product_id=None):
    object = Product.objects.get(id=product_id)
    object.delete()
    return redirect('manage_products')

@staff_member_required
def delete_vendor(request, vendor_id=None):
    vendor = Vendor.objects.get(id=vendor_id)
    object = User.objects.get(id=vendor.created_by.id)
    object.delete()
    return redirect('manage_vendors')

@staff_member_required
def admin_panel(request):
    return render(request, 'moderator/admin_panel.html')

@staff_member_required
def manage_categories(request):
    categories = Category.objects.all()
    return render(request, 'moderator/manage_categories.html', {'categories': categories})

@staff_member_required
def manage_products(request):
    products = Product.objects.all()
    return render(request, 'moderator/manage_products.html', {'products': products})

@staff_member_required
def manage_vendors(request):
    vendors = Vendor.objects.all()
    return render(request, 'moderator/manage_vendors.html', {'vendors': vendors})

@staff_member_required
def add_category(request):
    if request.method == 'POST':
        form = AddCategoryForm(request.POST)
        
        if form.is_valid():
            category_title = form.cleaned_data['title']
            category_slug = slugify(category_title)

            category = Category.objects.create(title=category_title, slug=category_slug, ordering=0)

            return redirect('manage_categories')
    else:
        form = AddCategoryForm()
    return render(request, 'moderator/add_category.html', {'form': form})

@login_required
def manage_orders(request):
    vendor = request.user.vendor
    #products = vendor.products.all()
    orders = vendor.orders.all()

    for order in orders:
        order.vendor_ammount = 0
        order.vendor_paid_amount = 0
        order.fully_paid = True

        for item in order.items.all():
            if item.vendor == request.user.vendor or request.user.is_staff :
                if item.vendor_paid:
                    order.vendor_paid_amount += item.get_total_price()
                else:
                    order.vendor_amount += item.get_total_price()
                    order.fully_paid = False

    return render(request, 'moderator/manage_orders.html', {'vendor': vendor, 'orders': orders})
