#
#
from re import template
from django.contrib.auth import views as auth_views
from django.urls import path

#
#

from . import views

#
#

urlpatterns = [
    path('', views.frontpage, name='frontpage'),
    path('contact/', views.contact, name='contact'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login')
]