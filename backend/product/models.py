from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

from mptt.managers import TreeManager
from mptt.models import MPTTModel
from measurement.measures import Weight
from django_measurement.models import MeasurementField

from . import ProductMediaTypes
from product.validators import validate_upc
from product.utils import generate_product_code, generate_upc_ean13, generate_upc_code, generate_ean13_code
from core import settings
from core.utils.image_path import upload_category_background_image, upload_product_media
from core.utils.weight import zero_weight
from core.units import WeightUnits
from core.models import SortableModel

class Category(MPTTModel):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.CASCADE
    )
    background_image = models.ImageField(upload_to=upload_category_background_image, blank=True, null=True)
    background_image_alt = models.CharField(max_length=128, blank=True)

    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def childrens(self):
        Category.objects.filter(parent=self)

    @property
    def any_children(self):
        return Category.objects.filter(parent=self).exists()
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = ('Categories')

class ProductType(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=128, unique=True, allow_unicode=True)
    has_variant = models.BooleanField(default=True)
    
    is_shipping_required = models.BooleanField(default=True)
    is_digital = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ('slug')
        verbose_name = _('Product Type')
        verbose_name_plural = ('Product Types')


class Product(models.Model):
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.CASCADE,
        related_name="pt_products"
    )
    uuid = models.UUIDField(default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    description = models.TextField(blank=True, null=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="ct_products",
        null=True,
        blank=True
    )

    weight = MeasurementField(
        measurement=Weight,
        unit_choices=WeightUnits.CHOICES,
        blank=True,
        null=True
    )
    
    default_variant = models.OneToOneField(
        "ProductVariant",
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
        blank=True,
    )

    rating = models.FloatField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_all_media(self):
        return self.media.all()

    def get_first_image(self):
        all_media = self.get_all_media()
        images = [media for media in all_media if media.type == ProductMediaTypes.IMAGE]
        return images[0] if images else None

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants"
    )
    
    #
    sku = models.CharField(max_length=64, unique=True)

    variant_code = models.CharField(max_length=5, unique=True, null=True, blank=True)
    upc_code = models.CharField(
        max_length=12,
        unique=True,
        validators=[validate_upc],
        null=True,
        blank=True
    )
    ean13_code = models.CharField(max_length=13, unique=True, null=True, blank=True)

    name = models.CharField(max_length=255, blank=True)

    weight = MeasurementField(
        measurement=Weight,
        unit_choices=WeightUnits.CHOICES,
        blank=True,
        null=True
    )

    quantity_limit_per_customer = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1)])

    #Price
    cost_price = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    selling_price = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        validators=[MinValueValidator(0)]
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_weight(self):
        return self.weight or self.product.weight
    
    def is_shipping_required(self) -> bool:
        return self.product.product_type.is_shipping_required
    
    def is_digital(self) -> bool:
        return self.product.product_type.is_digital

    def __str__(self) -> str:
        return self.name or self.sku or f'ID: {self.pk}'
    
    def save(self, *args, **kwargs):
        if not self.variant_code:
            self.variant_code = generate_product_code()        
        #self.upc_code, self.ean13_code = generate_upc_ean13(product_code=self.variant_code)
        if not self.upc_code:
            self.upc_code = generate_upc_code(product_code=self.variant_code)
        if not self.ean13_code:
            self.ean13_code = generate_ean13_code(product_code=self.variant_code)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = _('Product Variant')
        verbose_name_plural = _('Product Variants')

class ProductMedia(SortableModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="media"
    )

    image = models.ImageField(upload_to=upload_product_media, null=True, blank=True)
    alt = models.CharField(max_length=255, blank=True)
    media_type = models.CharField(
        max_length=32,
        choices=ProductMediaTypes.CHOICES,
        default=ProductMediaTypes.IMAGE
    )
    external_url = models.CharField(max_length=255, null=True, blank=True)

    def get_ordering_queryset(self):
        if not self.product:
            return ProductMedia.objects.none()
        # return self.product.media.all()
        return self.product.media.select_related('product').all()
    
    def __str__(self) -> str:
        return f"{self.product}'s media"
    
    class Meta:
        ordering = ('sort_order', 'pk')
        verbose_name = _('Product Media')
        verbose_name_plural = _('Product Media')

class VariantMedia(models.Model):
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="variant_media"
    )
    media = models.ForeignKey(
        ProductMedia,
        on_delete=models.CASCADE,
        related_name="m_variant_media"
    )

    def __str__(self) -> str:
        return f"{self.variant}'s media object"

    class Meta:
        unique_together = ("variant", "media")
        verbose_name = _('Product Variant Media')
        verbose_name_plurals = _('Product Variant Media')

    
    






