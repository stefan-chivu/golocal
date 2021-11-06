from apps.cart.cart import Cart

from .models import Order, OrderItem

def checkout(request, client, first_name, last_name, email, address, zipcode, phone, amount):
    order = Order.objects.create(client=client, first_name=first_name, last_name=last_name, email=email, address=address, zipcode=zipcode, phone=phone, vendor_paid_amount=amount, vendor_amount=0, total=0)

    total = 0
    for item in Cart(request):
        OrderItem.objects.create(order=order, product=item['product'], vendor=item['product'].vendor, price=item['product'].price, quantity=item['quantity'])

        order.vendors.add(item['product'].vendor)
        
    for item in order.items.all():
        total += item.get_total_price()

    order.total = total
    order.save()
    return order