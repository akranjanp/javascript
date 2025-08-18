from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.http import HttpResponseRedirect

from .models import (
    Attribute,
    AttributeValue,
    Product,
    ProductImage,
    ProductAttribute,
    ProductVariation,
    VariationAttributeValue,
    generate_variations_for_product,
)
from .forms import ProductAdminForm
from django import forms


class AttributeValueInline(admin.TabularInline):
    model = AttributeValue
    extra = 0


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [AttributeValueInline]


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image", "alt_text", "sort_order", "preview")
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" style="max-height:80px;"/>', obj.image.url)
        return ""


class ProductAttributeInlineForm(forms.ModelForm):
    class Meta:
        model = ProductAttribute
        fields = "__all__"


class ProductAttributeInline(admin.StackedInline):
    model = ProductAttribute
    form = ProductAttributeInlineForm
    extra = 0
    filter_vertical = ("values",)


class ProductVariationInline(admin.StackedInline):
    model = ProductVariation
    extra = 0
    fields = (
        "sku",
        ("regular_price", "sale_price"),
        ("manage_stock", "stock_quantity", "is_in_stock"),
        ("image", "image_preview"),
        ("option_key", "option_values"),
    )
    readonly_fields = ("image_preview", "option_key", "option_values")

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" style="max-height:80px;"/>', obj.image.url)
        return ""

    def option_values(self, obj):
        if not obj:
            return ""
        pairs = []
        for av in obj.selected_values.select_related("attribute").all():
            pairs.append(f"{av.attribute.name}: {av.name}")
        pairs.sort()
        return ", ".join(pairs)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    change_form_template = "admin/catalog/product/change_form.html"
    list_display = ("name", "product_type", "sku", "min_price", "max_price", "is_in_stock")
    list_filter = ("product_type", "is_in_stock")
    search_fields = ("name", "sku", "slug")
    prepopulated_fields = {"slug": ("name",)}

    fieldsets = (
        (None, {"fields": ("name", "slug", "product_type", "description")}),
        ("Pricing", {"fields": ("regular_price", "sale_price"), "classes": ("simple-only",)}),
        (
            "Inventory",
            {"fields": ("sku", "manage_stock", "stock_quantity", "is_in_stock"), "classes": ("simple-only",)},
        ),
        ("Images", {"fields": ("featured_image", "featured_preview")}),
    )

    readonly_fields = ("featured_preview",)

    inlines = [ProductImageInline, ProductAttributeInline, ProductVariationInline]

    def featured_preview(self, obj):
        if obj and obj.featured_image:
            return format_html('<img src="{}" style="max-height:120px;"/>', obj.featured_image.url)
        return ""

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                "<int:product_id>/generate-variations/",
                self.admin_site.admin_view(self.generate_variations_view),
                name="catalog_product_generate_variations",
            )
        ]
        return custom + urls

    def generate_variations_view(self, request, product_id: int):
        product = Product.objects.get(pk=product_id)
        created = generate_variations_for_product(product)
        self.message_user(request, f"Generated {created} new variations.")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/admin/"))

    actions = ["generate_variations_action"]

    def generate_variations_action(self, request, queryset):
        total_created = 0
        for product in queryset:
            total_created += generate_variations_for_product(product)
        self.message_user(request, f"Generated {total_created} new variations across selected products.")
    generate_variations_action.short_description = "Generate variations from attributes"


# Register your models here.
