from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# from apps.vendor.views import vendor_admin

# Create your models here.

class Vendor(models.Model):
    name = models.CharField(max_length=80)
    address = models.CharField(max_length=150, default="")
    phoneNo = PhoneNumberField(null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.OneToOneField(User, related_name='vendor', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_balance(self):
        items = self.items.filter(vendor_paid=False, order__vendors__in=[self.id])
        return sum(item.product.price * item.quantity for item in items)

    def get_paid_amount(self):
        items = self.items.filter(vendor_paid=True, order__vendors__in=[self.id])
        return sum(item.product.price * item.quantity for item in items)