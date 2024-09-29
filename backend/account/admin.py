from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from account.forms import CustomUserCreationForm
from account.models import (
    User,
    CustomerUser,
    Manager,
    Employee,
    Address
)

@admin.register(User)
class MyUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    fieldsets = (
        (_('Login Information'), {'fields': ('uuid', 'email', 'username', 'password')}),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_confirmed', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
            )
        }),
        (_('Requests'), {'fields': ('last_confirm_email_request', 'last_password_reset_request')}),
        (_('Profile Type'), {'fields': ('is_customer', 'is_manager', 'is_employee')}),
        (_('Dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # ADD USER FIELD
    add_fieldsets = (
        (_('Login Information'), {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

    list_display = ('uuid', 'email', 'username', 'is_staff')
    list_filter = ('is_active', 'is_confirmed', 'is_staff', 'is_superuser')
    search_fields = ('uuid', 'email', 'username')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('date_joined',)
    filter_horizontal = (
        'groups',
        'user_permissions',
    )

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Main Information'), {'fields': ('uuid', 'user', 'address_name')}),
        (_('Personal Information'),
         {'fields': ('first_name', 'last_name', 'company_name', 'phone')}),
        (_('Address'), {
            'fields': ('street_address_1', 'street_address_2', 'postal_code', 'city', 'city_area', 'country', 'country_area')
        })
    )

    list_display = ('address_name', 'user', 'city', 'city_area', 'country')
    # list_filter = ('country',)
    search_fields = (
        'uuid', 
        'address_name', 
        'user__email__icontains',
        'first_name__icontains',
        'last_name__icontains',
        'company_name__icontains',
        'phone'
    )

@admin.register(CustomerUser)
class CustomerUserAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('User'), {'fields': ('user',)}),
        (_('Personal Information'), {'fields': ('first_name', 'last_name', 'phone')}),
        (_('Default Addresses'), {'fields': ('default_shipping_address', 'default_billing_address')}),
        (_('Note'), {'fields': ('note',)}),
    )

    list_display = ('user', 'first_name', 'last_name', 'phone')
    search_fields = ('user__email__icontains', 'first_name', 'last_name', 'phone')

admin.site.register(Manager)
admin.site.register(Employee)