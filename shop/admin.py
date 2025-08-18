from django.contrib import admin
from django.utils.html import format_html
from django import forms

from .models import (
    Product,
    ProductGalleryImage,
    Attribute,
    AttributeValue,
    ProductAttribute,
    ProductVariation,
)


class ProductGalleryInline(admin.TabularInline):
    model = ProductGalleryImage
    extra = 1
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 100px;" />', obj.image.url)
        return ""


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1


class ProductVariationInline(admin.TabularInline):
    model = ProductVariation
    extra = 0
    readonly_fields = ("preview",)
    fields = ("values", "sku", "regular_price", "sale_price", "image", "preview", "manage_stock", "stock_quantity", "stock_status")
    filter_horizontal = ("values",)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 100px;" />', obj.image.url)
        return ""


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        product_type = self.instance.product_type if self.instance.pk else self.initial.get("product_type", Product.SIMPLE)

        # Hide/show fields depending on product type
        if product_type == Product.SIMPLE:
            # hide variable-only fields handled via inlines
            self.fields.pop("manage_stock", None)  # keep still
        elif product_type == Product.VARIABLE:
            # For variable product, hide pricing fields as they will be on variations
            for field in ["regular_price", "sale_price", "sku", "stock_quantity", "stock_status"]:
                self.fields[field].widget = forms.HiddenInput()
                self.fields[field].required = False


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ("name", "product_type", "regular_price", "sale_price", "stock_status")
    search_fields = ("name", "slug", "sku")
    inlines = [ProductGalleryInline, ProductAttributeInline, ProductVariationInline]
    fieldsets = (
        (None, {
            "fields": ("name", "slug", "product_type", "feature_image")
        }),
        ("Pricing", {
            "fields": ("regular_price", "sale_price")
        }),
        ("Inventory", {
            "fields": ("sku", "manage_stock", "stock_quantity", "stock_status")
        }),
    )

    class Media:
        js = [
            "shop/js/admin/product_admin.js",  # Provide dynamic show/hide script
        ]


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name", "slug")


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ("attribute", "value")
    list_filter = ("attribute",)
    search_fields = ("value",)