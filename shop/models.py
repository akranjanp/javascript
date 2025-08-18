from django.db import models
from django.template.defaultfilters import slugify
from django.core.validators import MinValueValidator
from itertools import product as cartesian_product


class TimestampedModel(models.Model):
    """Abstract base model with created/updated timestamps."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(TimestampedModel):
    SIMPLE = "simple"
    VARIABLE = "variable"
    PRODUCT_TYPE_CHOICES = (
        (SIMPLE, "Simple"),
        (VARIABLE, "Variable"),
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES, default=SIMPLE)

    # Pricing
    regular_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True)

    sku = models.CharField(max_length=64, unique=True)

    # Stock management
    manage_stock = models.BooleanField(default=True)
    stock_quantity = models.PositiveIntegerField(null=True, blank=True)
    stock_status = models.CharField(
        max_length=20,
        choices=(
            ("instock", "In stock"),
            ("outofstock", "Out of stock"),
            ("onbackorder", "On backorder"),
        ),
        default="instock",
    )

    # Images
    feature_image = models.ImageField(upload_to="products/feature/", null=True, blank=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    # --------- Variable product helpers ---------
    def is_variable(self):
        return self.product_type == self.VARIABLE

    def generate_variations(self):
        """Generate variations for all combinations of selected attribute values."""
        if not self.is_variable():
            return
        attribute_sets = []
        for pattr in self.product_attributes.prefetch_related("values"):
            values = list(pattr.values.all())
            if values:
                attribute_sets.append(values)
        for combo in cartesian_product(*attribute_sets):
            # Check if variation exists
            if not ProductVariation.objects.filter(product=self, values__in=combo).exists():
                variation = ProductVariation.objects.create(product=self)
                variation.values.set(combo)


class ProductGalleryImage(TimestampedModel):
    product = models.ForeignKey(Product, related_name="gallery_images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/gallery/")

    def __str__(self):
        return f"Image for {self.product.name}"


class Attribute(TimestampedModel):
    """Global attribute e.g., Size, Color"""

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        ordering = ("name",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class AttributeValue(TimestampedModel):
    attribute = models.ForeignKey(Attribute, related_name="values", on_delete=models.CASCADE)
    value = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, blank=True)

    class Meta:
        unique_together = ("attribute", "value")
        ordering = ("attribute__name", "value")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.value)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


class ProductAttribute(TimestampedModel):
    """Attribute enabled for a given product"""

    product = models.ForeignKey(Product, related_name="product_attributes", on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    values = models.ManyToManyField(AttributeValue, blank=True)
    use_for_variations = models.BooleanField(default=False)

    class Meta:
        unique_together = ("product", "attribute")

    def __str__(self):
        return f"{self.product.name} - {self.attribute.name}"


class ProductVariation(TimestampedModel):
    """Variation of a variable product"""

    product = models.ForeignKey(Product, related_name="variations", on_delete=models.CASCADE)
    values = models.ManyToManyField(AttributeValue, related_name="variations", blank=True)

    sku = models.CharField(max_length=64, unique=True, null=True, blank=True)
    regular_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True)
    image = models.ImageField(upload_to="products/variations/", null=True, blank=True)

    manage_stock = models.BooleanField(default=True)
    stock_quantity = models.PositiveIntegerField(null=True, blank=True)
    stock_status = models.CharField(
        max_length=20,
        choices=(
            ("instock", "In stock"),
            ("outofstock", "Out of stock"),
            ("onbackorder", "On backorder"),
        ),
        default="instock",
    )

    class Meta:
        unique_together = ("product",)

    def __str__(self):
        attrs = ", ".join([v.value for v in self.values.all()])
        return f"{self.product.name} - {attrs}" if attrs else f"Variation of {self.product.name}"