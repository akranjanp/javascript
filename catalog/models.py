from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Attribute(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            unique = base
            idx = 2
            while Attribute.objects.filter(slug=unique).exclude(pk=self.pk).exists():
                unique = f"{base}-{idx}"
                idx += 1
            self.slug = unique
        super().save(*args, **kwargs)


class AttributeValue(TimeStampedModel):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name="values")
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, blank=True)

    class Meta:
        unique_together = ("attribute", "slug")
        ordering = ["attribute__name", "name"]

    def __str__(self) -> str:
        return f"{self.attribute.name}: {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            unique = base
            idx = 2
            while AttributeValue.objects.filter(attribute=self.attribute, slug=unique).exclude(pk=self.pk).exists():
                unique = f"{base}-{idx}"
                idx += 1
            self.slug = unique
        super().save(*args, **kwargs)


class Product(TimeStampedModel):
    class ProductType(models.TextChoices):
        SIMPLE = "simple", _("Simple")
        VARIABLE = "variable", _("Variable")

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    description = models.TextField(blank=True)
    product_type = models.CharField(max_length=20, choices=ProductType.choices, default=ProductType.SIMPLE)

    # Pricing
    regular_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # SKU and stock (for simple only; for variable use variations)
    sku = models.CharField(max_length=64, unique=True, null=True, blank=True)
    manage_stock = models.BooleanField(default=False)
    stock_quantity = models.IntegerField(null=True, blank=True)
    is_in_stock = models.BooleanField(default=True)

    # Images
    featured_image = models.ImageField(upload_to="products/featured/", blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.name

    def clean(self):
        errors = {}
        if self.product_type == Product.ProductType.SIMPLE:
            # Simple product must have base pricing
            if self.regular_price is None:
                errors["regular_price"] = _("Regular price is required for simple products.")
            if self.manage_stock and self.stock_quantity is None:
                errors["stock_quantity"] = _("Stock quantity required when stock management is enabled.")
        else:
            # Variable product should not carry simple-only fields
            if self.regular_price is not None or self.sale_price is not None:
                pass  # allowed as base price fallback, keep optional
            if self.manage_stock or self.stock_quantity is not None:
                errors["manage_stock"] = _("Stock is managed at variation level for variable products.")
            # SKU optional on parent, but must not collide with variation SKUs
        if self.sale_price is not None and self.regular_price is not None:
            if self.sale_price >= self.regular_price:
                errors["sale_price"] = _("Sale price must be less than regular price.")
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            unique = base
            idx = 2
            while Product.objects.filter(slug=unique).exclude(pk=self.pk).exists():
                unique = f"{base}-{idx}"
                idx += 1
            self.slug = unique
        super().save(*args, **kwargs)

    @property
    def min_price(self):
        if self.product_type == Product.ProductType.SIMPLE:
            return self.sale_price or self.regular_price
        # variable: min over variations
        prices = [v.sale_price or v.regular_price for v in self.variations.all() if (v.sale_price or v.regular_price) is not None]
        return min(prices) if prices else None

    @property
    def max_price(self):
        if self.product_type == Product.ProductType.SIMPLE:
            return self.regular_price
        prices = [v.regular_price for v in self.variations.all() if v.regular_price is not None]
        return max(prices) if prices else None


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="gallery")
    image = models.ImageField(upload_to="products/gallery/")
    alt_text = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self) -> str:
        return f"Image for {self.product.name}"


class ProductAttribute(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_attributes")
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    values = models.ManyToManyField(AttributeValue, related_name="product_attribute_values", blank=True)
    use_for_variations = models.BooleanField(default=False)

    class Meta:
        unique_together = ("product", "attribute")
        verbose_name = _("Product attribute")
        verbose_name_plural = _("Product attributes")

    def __str__(self) -> str:
        return f"{self.product.name} - {self.attribute.name}"


class ProductVariation(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variations")
    option_key = models.CharField(max_length=512, blank=True, help_text=_("Internal key built from selected attribute values"))

    # Variation specifics
    sku = models.CharField(max_length=64, unique=True)
    regular_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    manage_stock = models.BooleanField(default=False)
    stock_quantity = models.IntegerField(null=True, blank=True)
    is_in_stock = models.BooleanField(default=True)
    image = models.ImageField(upload_to="products/variations/", blank=True, null=True)

    selected_values = models.ManyToManyField(AttributeValue, through="VariationAttributeValue", related_name="variations")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["product", "option_key"], name="unique_variation_option_key_per_product"),
        ]

    def __str__(self) -> str:
        return f"{self.product.name} ({self.option_key or 'custom'})"

    def clean(self):
        errors = {}
        if self.manage_stock and self.stock_quantity is None:
            errors["stock_quantity"] = _("Stock quantity required when stock management is enabled.")
        if self.sale_price is not None and self.regular_price is not None:
            if self.sale_price >= self.regular_price:
                errors["sale_price"] = _("Sale price must be less than regular price.")
        if errors:
            raise ValidationError(errors)

    def build_option_key(self) -> str:
        pairs = []
        # Use current related values if saved; otherwise leave blank
        for av in self.selected_values.select_related("attribute").all():
            pairs.append(f"{av.attribute_id}:{av.id}")
        pairs.sort()
        return "|".join(pairs)

    def save(self, *args, **kwargs):
        # option_key will be built after save when M2M is available; allow blank on initial save
        super().save(*args, **kwargs)
        current = self.build_option_key()
        if current and self.option_key != current:
            ProductVariation.objects.filter(pk=self.pk).update(option_key=current)
            self.option_key = current


class VariationAttributeValue(models.Model):
    variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("variation", "attribute_value")

    def __str__(self) -> str:
        return f"{self.variation} -> {self.attribute_value}"


def generate_variations_for_product(product: Product) -> int:
    """Generate all possible variations based on product attributes flagged for variations.

    Returns the number of variations created.
    """
    if product.product_type != Product.ProductType.VARIABLE:
        return 0

    from itertools import product as iter_product

    selectable = list(
        product.product_attributes.filter(use_for_variations=True).prefetch_related("values", "attribute")
    )
    value_lists = []
    for pa in selectable:
        values = list(pa.values.all())
        if not values:
            continue
        # represent as [(attribute_id, AttributeValue), ...]
        value_lists.append([(pa.attribute_id, v) for v in values])

    if not value_lists:
        return 0

    created_count = 0
    for combo in iter_product(*value_lists):
        # Build deterministic option_key
        parts = [f"{attr_id}:{av.id}" for (attr_id, av) in combo]
        parts.sort()
        option_key = "|".join(parts)
        # Skip if exists
        if ProductVariation.objects.filter(product=product, option_key=option_key).exists():
            continue
        # Create skeleton variation; SKU left to admin to fill manually; ensure uniqueness by temporary placeholder
        temp_sku = f"{product.id}-var-{created_count+1}"
        variation = ProductVariation.objects.create(product=product, option_key=option_key, sku=temp_sku)
        for (_, av) in combo:
            VariationAttributeValue.objects.create(variation=variation, attribute_value=av)
        created_count += 1

    return created_count
