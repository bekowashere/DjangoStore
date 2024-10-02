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
from core import settings
from core.utils.image_path import upload_category_background_image
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
    #  default_variant

    rating = models.FloatField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def get_first_image

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')



    
    






