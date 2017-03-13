from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator
from django.utils.timezone import now


def valid_birthday(value):
    minus_120_years = now().date().replace(year=now().year-120)
    if (value > now().date()) or (value < minus_120_years):
        raise ValidationError("Enter your real date of birth!")
    return "OK"


def valid_name(val):
    if not val.isalpha():
        raise ValidationError("Enter a valid name.")
    return "OK"

valid_skype = RegexValidator(r'^[0-9a-zA-Z_]*$', 'Enter a valid skype.')
valid_jabber = EmailValidator('Enter a valid jabber.')
