from django.urls import path

from . import views

urlpatterns = [
    path('become-vendor/', views.become_vendor, name='become_vendor'),
    path('vendor_admin/', views.vendor_admin, name='vendor_admin'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit-vendor/', views.edit_vendor, name='edit_vendor'),
    path('<int:vendor_id>/', views.vendor, name='vendor'),
]
