from django.urls import path

from . import views

urlpatterns = [
    path('', views.admin_panel, name='moderator'),
    path('delete/category/<int:category_id>', views.delete_category, name='delete_category'),
    path('delete/product/<int:product_id>', views.delete_product, name='delete_product'),
    path('delete/vendor/<int:vendor_id>', views.delete_vendor, name='delete_vendor'),
    path('add-category/', views.add_category, name='add_category'),
    path('manage-categories/', views.manage_categories, name='manage_categories'),
    path('manage-products/', views.manage_products, name='manage_products'),
    path('manage-vendors/', views.manage_vendors, name='manage_vendors'),
]
