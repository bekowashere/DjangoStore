from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from product.models import (
    Category,
    ProductType,
    Product,
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

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Main Information'), {
            'fields': (
                'product_type', 'category', 'uuid', 'name', 'slug', 'is_active', 'default_variant'
            )
        }),
        (_('Specifications'), {'fields': ('weight', 'rating')}),
        (_('Description'), {'fields': ('description',)}),
        (_('Dates'), {'fields': ('created_at', 'updated_at')}),
    )

    list_display = ('uuid', 'name', 'slug')
    list_filter = ('uuid', 'name__icontains', 'slug')
    search_fields = ('uuid', 'email', 'username')
    readonly_fields = ('uuid',)
    ordering = ('created_at',)