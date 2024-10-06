from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from product.models import (
    Category,
    ProductType,
    ProductVariant,
    ProductMedia,
    VariantMedia
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Main Information'), {'fields': ('name', 'slug', 'parent')}),
        (_('Description'), {'fields': ('description',)}),
        (_('Image'), {'fields': ('background_image', 'background_image_alt')}),
        (_('Dates'), {'fields': ('updated_at',)}),
    )

    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    ordering = ('name',)