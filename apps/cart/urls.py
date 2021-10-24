from django.urls import path

from . import views

urlpatterns = [
    path('', views.cart_detail, name='cart'),
    path('place_order', views.place_order, name='place_order'),
    path('success', views.success, name='success'),
]
