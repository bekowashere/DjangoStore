from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from world.models import Currency, Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('General Information'), {'fields': ('name', 'iso3', 'iso2')}),
        (_('Code Information'), {'fields': ('numeric_code', 'phone_code', 'tld')}),
        (_('Currency Information'), {'fields': ('currency',)}),
        (_('Timezones'), {'fields': ('timezones',)}),
        (_('Geographic Information'), {'fields': ('native', 'region', 'subregion', 'capital')}),
        (_('Location Information'), {'fields': ('latitude', 'longitude')}),
        (_('Emoji'), {'fields': ('emoji', 'emojiU')}),
    )

    list_display = ('name', 'iso2', 'iso3', 'phone_code')
    list_filter = ('region',)
    search_fields = ('name', 'iso2', 'iso3')


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('currency_name', 'currency_code', 'currency_symbol')
    search_fields = ('currency_name', 'currency_code')