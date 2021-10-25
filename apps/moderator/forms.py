from django.forms import ModelForm

from apps.product.models import Category

class AddCategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['title']