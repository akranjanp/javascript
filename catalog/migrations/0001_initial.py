from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=120, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=140, unique=True)),
            ],
            options={'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=120)),
                ('slug', models.SlugField(blank=True, max_length=140)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='values', to='catalog.attribute')),
            ],
            options={'ordering': ['attribute__name', 'name']},
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=280, unique=True)),
                ('description', models.TextField(blank=True)),
                ('product_type', models.CharField(choices=[('simple', 'Simple'), ('variable', 'Variable')], default='simple', max_length=20)),
                ('regular_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('sale_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('sku', models.CharField(blank=True, max_length=64, null=True, unique=True)),
                ('manage_stock', models.BooleanField(default=False)),
                ('stock_quantity', models.IntegerField(blank=True, null=True)),
                ('is_in_stock', models.BooleanField(default=True)),
                ('featured_image', models.ImageField(blank=True, null=True, upload_to='products/featured/')),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('use_for_variations', models.BooleanField(default=False)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.attribute')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_attributes', to='catalog.product')),
            ],
            options={'verbose_name': 'Product attribute', 'verbose_name_plural': 'Product attributes'},
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='products/gallery/')),
                ('alt_text', models.CharField(blank=True, max_length=255)),
                ('sort_order', models.PositiveIntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery', to='catalog.product')),
            ],
            options={'ordering': ['sort_order', 'id']},
        ),
        migrations.CreateModel(
            name='ProductVariation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('option_key', models.CharField(blank=True, help_text='Internal key built from selected attribute values', max_length=512)),
                ('sku', models.CharField(max_length=64, unique=True)),
                ('regular_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('sale_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('manage_stock', models.BooleanField(default=False)),
                ('stock_quantity', models.IntegerField(blank=True, null=True)),
                ('is_in_stock', models.BooleanField(default=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/variations/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variations', to='catalog.product')),
            ],
        ),
        migrations.CreateModel(
            name='VariationAttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute_value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.attributevalue')),
                ('variation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.productvariation')),
            ],
        ),
        migrations.AddField(
            model_name='productvariation',
            name='selected_values',
            field=models.ManyToManyField(related_name='variations', through='catalog.VariationAttributeValue', to='catalog.attributevalue'),
        ),
        migrations.AddConstraint(
            model_name='productvariation',
            constraint=models.UniqueConstraint(fields=('product', 'option_key'), name='unique_variation_option_key_per_product'),
        ),
        migrations.AddField(
            model_name='productattribute',
            name='values',
            field=models.ManyToManyField(blank=True, related_name='product_attribute_values', to='catalog.attributevalue'),
        ),
        migrations.AlterUniqueTogether(
            name='variationattributevalue',
            unique_together={('variation', 'attribute_value')},
        ),
        migrations.AlterUniqueTogether(
            name='productattribute',
            unique_together={('product', 'attribute')},
        ),
        migrations.AlterUniqueTogether(
            name='attributevalue',
            unique_together={('attribute', 'slug')},
        ),
    ]

