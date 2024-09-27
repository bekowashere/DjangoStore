from django.db import models
import uuid
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from core.utils.image_path import upload_person_portrait, upload_person_credentials

# MODELS
from world.models import Country
from inventory.models import Warehouse

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
    is_staff = models.BooleanField(_('Staff User'), default=False)
    is_superuser = models.BooleanField(_('Superuser'), default=False)

    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    last_login = models.DateTimeField(auto_now=True)

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
class Address(models.Model):
    pass

class CustomerUser(models.Model):
    pass

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
        _('Ident'),
        upload_to=upload_person_credentials,
        null=True,
        blank=True
    )

    class Meta:
        abstract = True

# WarehouseManager modelinde warehouse değiştirdiğimiz zaman signals ile Warehouseun manager fieldına etki ettir.
class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name=_('User'))
    warehouse = models.OneToOneField(
        Warehouse,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='manager',
        verbose_name=_('Warehouse'),
    )

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name=_('User'))
    position = models.CharField(_('Position'), max_length=64, default="Warehouse Attendant")
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.SET_NULL,
        related_name='wh_employees',
        verbose_name=_('Warehouse'),
        null=True
    )

