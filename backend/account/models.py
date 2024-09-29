from uuid import uuid4
from functools import partial

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.forms.models import model_to_dict
from django.core.validators import FileExtensionValidator
from core.utils.image_path import upload_person_portrait, upload_person_credentials
from phonenumber_field.modelfields import PhoneNumber, PhoneNumberField

from world.models import Country
from inventory.models import Warehouse
from account.validators import validate_possible_number

class PossiblePhoneNumberField(PhoneNumberField):
    default_validators = [validate_possible_number]

class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with given email and password
        """

        if not email:
            raise ValueError(_('You must provide an email address'))

        if not password:
            raise ValueError(_('User must have a password'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user = self._create_user(email, password=password, **extra_fields)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))

        user = self._create_user(email, password=password, **extra_fields)
        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(default=uuid4, unique=True)
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('Username'),
        max_length=64,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        }
    )

    email = models.EmailField(
        _('Email Address'),
        unique=True,
        help_text=_('Required. 50 characters or fewer. Example: john.doe@gmail.com'),
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )

    is_active = models.BooleanField(_('Active'), default=True)
    is_confirmed = models.BooleanField(_('Confirmed'), default=True)
    is_staff = models.BooleanField(_('Staff User'), default=False)
    is_superuser = models.BooleanField(_('Superuser'), default=False)

    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    last_login = models.DateTimeField(auto_now=True)

    #
    # jwt_token_key = models.CharField(max_length=12, default=partial(get_random_string, length=12))
    last_confirm_email_request = models.DateTimeField(null=True, blank=True)
    last_password_reset_request = models.DateTimeField(null=True, blank=True)

    # !!
    is_customer = models.BooleanField(_('Customer'), default=False)
    is_manager = models.BooleanField(_('Manager'), default=False)
    is_employee = models.BooleanField(_('Employee'), default=False)
    

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.get_username()
    
    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')

# LOOK
# Set as default shipping address
# Set as default billing address
class Address(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True)
    user = models.ForeignKey(
        'account.CustomerUser',
        on_delete=models.CASCADE,
        related_name='customer_addresses',
        verbose_name=_('Customer')
    )
    address_name = models.CharField(_('Address Name'), max_length=64, help_text="Ex: Home")
    first_name = models.CharField(_('First Name'), max_length=64)
    last_name = models.CharField(_('Last Name'), max_length=64)
    company_name = models.CharField(_('Company Name'), max_length=64, null=True, blank=True)
    phone = PossiblePhoneNumberField(_('Phone'), blank=True, default="", db_index=True)
    street_address_1 = models.CharField(_('Street Address 1'), max_length=256, blank=True)
    street_address_2 = models.CharField(_('Street Address 2'), max_length=256, blank=True)
    city = models.CharField(('City'), max_length=256, blank=True, help_text='Los Angeles')
    city_area = models.CharField(_('City Area'), max_length=128, blank=True, help_text='California')
    postal_code = models.CharField(_('Postal Code'), max_length=20, blank=True)
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        related_name='country_addresses',
        verbose_name=_('Country'),
        null=True
    )
    country_area = models.CharField(_('Country Area'), max_length=128, blank=True, help_text='Northern America')

    def __str__(self) -> str:
        return self.address_name
    
    @property
    def fullname(self):
        fn = f'{self.first_name} {self.last_name}'
        return fn
    
    def as_data(self):
        """
        Return the address as a dict
        Result does not contain the primary key(id)
        """
        data = model_to_dict(self, exclude=["id"])
        return data

    
    def get_copy(self):
        """Return a new instance of the same address"""
        return Address.objects.create(**self.as_data())
    
    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

class CustomerUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name=_('User'),
        related_name='customer_profile'
    )

    first_name = models.CharField(_('First Name'), max_length=64, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=64, blank=True)
    phone = PossiblePhoneNumberField(_('Phone'), blank=True, default="")

    # Address
    default_shipping_address = models.OneToOneField(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Default Shipping Address'),
        related_name="+",
    )

    default_billing_address = models.OneToOneField(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Default Billing Address'),
        related_name="+",
    )

    note = models.TextField(_('Note') ,null=True, blank=True)

    def get_full_name(self):
        if self.first_name or self.last_name:
            return f'{self.first_name} {self.last_name}'.strip()
        if self.default_shipping_address:
            first_name = self.default_shipping_address.first_name
            last_name = self.default_shipping_address.last_name
            if first_name or last_name:
                return f'{first_name} {last_name}'.strip()
        return self.user.email

# STAFF
class Person(models.Model):
    first_name = models.CharField(_('First Name'), max_length=32)
    last_name = models.CharField(_('Last Name'), max_length=32)
    number = models.CharField(_('Number'), max_length=8)

    identification_number = models.CharField(_('Identification Number'), max_length=11, unique=True, null=True, blank=True)
    phone_number = models.CharField(_('Phone'), max_length=10, null=True, blank=True) #Regex ile sayı?
    birth_date = models.DateField(_('Birthdate'), null=True, blank=True)

    # Files
    portrait = models.FileField(
        _('Portrait'),
        upload_to=upload_person_portrait,
        null=True,
        blank=True
    )

    credentials = models.FileField(
        _('Credentials'),
        upload_to=upload_person_credentials,
        null=True,
        blank=True
    )

    class Meta:
        abstract = True

# signals Warehouse, Manager, Employee
class Manager(Person):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name=_('User'))
    warehouse = models.OneToOneField(
        Warehouse,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='manager',
        verbose_name=_('Warehouse'),
    )

    def get_employees(self):
        return self.mn_employees.all()
    
    @property
    def employee_count(self):
        return self.get_employees().count()

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

class Employee(Person):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name=_('User'))
    position = models.CharField(_('Position'), max_length=64, default="Warehouse Attendant")
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.SET_NULL,
        related_name='wh_employees',
        verbose_name=_('Warehouse'),
        null=True
    )
    manager = models.ForeignKey(
        Manager,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mn_employees',
        verbose_name=_('Manager')
    )

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

