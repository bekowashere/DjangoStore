from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _

# MODELS
from world.models import Country

# Create your models here.
class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('Location Name'), max_length=64, unique=True)
    address_line = models.CharField(_('Street Address 1'), max_length=256)
    postal_code = models.CharField(_('Postal Code'), max_length=32)
    city = models.CharField(_('City'), max_length=64, help_text="Ex: Los Angeles")
    city_area = models.CharField(_('City Area'), max_length=64, help_text="Ex: California")
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        related_name='locations',
        verbose_name=_('Country'),
        null=True
    )
    latitude = models.FloatField(_('Latitude'), null=True, blank=True)
    longitude = models.FloatField(_('Longitude'), null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.name} - {self.city}'

class Warehouse(models.Model):
    name = models.CharField(_('Warehouse Name'), max_length=64, unique=True)
    main = models.BooleanField(_('Main'), default=False)
    capacity = models.PositiveSmallIntegerField(_('Capacity'), null=True, blank=True)
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        related_name='warehouses',
        verbose_name=_('Location'),
        null=True
    )
