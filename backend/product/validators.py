from django.core.exceptions import ValidationError

from django.core.exceptions import ValidationError

def validate_upc(value):
    if len(value) != 12:
        raise ValidationError("UPC must be 12 digits long.")
    if not value.isdigit():
        raise ValidationError("UPC must contain only numbers.")