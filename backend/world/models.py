from django.db import models
from django.utils.translation import gettext_lazy as _

class Currency(models.Model):
    currency_code = models.CharField(_('Currency Code'), max_length=3)
    currency_name = models.CharField(_('Currency Name'), max_length=64)
    currency_symbol = models.CharField(_('Currency Symbol'), max_length=8)

    def __str__(self):
        return self.currency_code

    class Meta:
        ordering = ['currency_name']
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')

class Timezone(models.Model):
    zoneName = models.CharField(_('Timezone Name'), max_length=64)
    gmtOffset = models.CharField(max_length=8)
    gmtOffsetName = models.CharField(max_length=16)
    abbreviation = models.CharField(max_length=4)
    tzName = models.CharField(max_length=64)

    def __str__(self):
        return self.zoneName

    class Meta:
        verbose_name = _('Timezone')
        verbose_name_plural = _('Timezones')

class Country(models.Model):
    name = models.CharField(_('Country Name'), max_length=255)
    iso3 = models.CharField(_('ISO3'), max_length=3)
    iso2 = models.CharField(_('ISO2'), max_length=2)
    numeric_code = models.CharField(_('Numeric Code'), max_length=4)
    phone_code = models.CharField(_('Phone Code'), max_length=8)
    capital = models.CharField(_('Capital'), max_length=64)
    currency = models.ForeignKey(
        Currency,
        on_delete=models.SET_NULL,
        related_name='currency_countries',
        null=True,
        blank=True,
    )
    tld = models.CharField(_('TLD'), max_length=8)
    native = models.CharField(_('Native'), max_length=255)
    region = models.CharField(_('Region'), max_length=64)
    subregion = models.CharField(_('Sub Region'), max_length=64)
    timezones = models.ManyToManyField(Timezone, verbose_name=_('Timezones'), blank=True)
    latitude = models.DecimalField(_('Latitude'), max_digits=11, decimal_places=8)
    longitude = models.DecimalField(_('Longitude'), max_digits=11, decimal_places=8)
    emoji = models.CharField(_('Emoji'), max_length=2)
    emojiU = models.CharField(_('Emoji U'), max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')