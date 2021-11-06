from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.admin.views.decorators import staff_member_required
from slugify import slugify

from apps.moderator.forms import AddCategoryForm

from apps.product.models import Category, Product
from apps.vendor.forms import ProductForm
from apps.vendor.models import Vendor
from apps.order.models import Order

@staff_member_required
def delete_category(request, category_id=None):
    object = Category.objects.get(id=category_id)
    object.delete()
    return redirect('manage_categories')

@staff_member_required
def edit_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)

    if request.method == 'POST':
        title = request.POST.get('title', '')

        if title:
            category.title = title
            category.slug = slugify(title)
            category.save()

            return redirect('manage_categories')

    return render(request, 'moderator/edit_category.html', {'category':category})

@login_required
def edit_product(request, product_id):
    product=get_object_or_404(Product, id=product_id)

    if request.user.vendor == product.vendor or request.user.is_staff:

        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)

            if form.is_valid():
                product = form.save(commit=False)
                product.slug = slugify(product.title)
                product.save()

                if request.user.vendor == product.vendor:
                    return redirect('vendor_admin')
                else:
                    return redirect('manage_products')
        else:
            form = ProductForm(instance=product)

        return render(request, 'moderator/edit_product.html', {'product': product, 'form': form, 'product_id': product_id})
    else:
        return render(request, 'core/access_denied.html')

@login_required
def delete_product(request, product_id=None):
    object = Product.objects.get(id=product_id)
    if request.user.is_staff or request.user.vendor == object.vendor:
        object.delete()
        if request.user.is_staff:
            return redirect('manage_products')
        else:
            return redirect('vendor_admin')
    else:
        return render(request, 'core/access_denied.html')

@staff_member_required
def delete_order(request, order_id=None):
    object = Order.objects.get(id=order_id)
    object.delete()
    return redirect('manage_orders')

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
    if request.user.is_staff:
        orders = Order.objects.all()
    else:
        orders = vendor.orders.all()

    placed_orders = Order.objects.all().filter(client=request.user.vendor)

    for order in orders:
        order.vendor_ammount = 0
        order.vendor_paid_amount = 0
        order.fully_paid = True

        for item in order.items.all():
            if item.vendor == request.user.vendor or request.user.is_staff:
                if item.vendor_paid:
                    order.vendor_paid_amount += item.get_total_price()
                else:
                    order.vendor_amount += item.get_total_price()
                    order.fully_paid = False

    return render(request, 'moderator/manage_orders.html', {'vendor': vendor, 'orders': orders, 'placed_orders': placed_orders})
