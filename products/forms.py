from django import forms
from django.forms import inlineformset_factory
from .models import CompanyProducts, CompanyProductsImages
class ProductForm(forms.ModelForm):
    class Meta:
        model=CompanyProducts
        fields=['product_name', 'product_description', 'product_quantity', 'product_price', 'product_discount']
CompanyProductsImagesFormSet = inlineformset_factory(
    CompanyProducts,
    CompanyProductsImages,
    fields=('product_image',),
    extra=3,  # Number of extra forms to display.
    can_delete=True
)
