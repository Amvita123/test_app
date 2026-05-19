import phonenumbers
from django.core.exceptions import ValidationError

def validate_phone_number(value):
    if not value.startswith('+'):
        value = '+' + value

    try:
        number = phonenumbers.parse(value, None)
        if not phonenumbers.is_possible_number(number):
            raise ValidationError('Phone number is not possible')
        if not phonenumbers.is_valid_number(number):
            raise ValidationError('Phone number is not valid')

    except phonenumbers.NumberParseException:
        raise ValidationError('Use +<countrycode><number> (e.g. +919876543210).')