from django import forms
from django.core.exceptions import ValidationError

from .models import Product


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def clean(self):
        cleaned = super().clean()
        product_type = cleaned.get("product_type")
        sku = cleaned.get("sku")
        if product_type == Product.ProductType.SIMPLE and not sku:
            raise ValidationError({"sku": "SKU is required for simple products."})
        if product_type == Product.ProductType.VARIABLE and cleaned.get("manage_stock"):
            raise ValidationError({"manage_stock": "Stock is managed at variation level for variable products."})
        return cleaned

