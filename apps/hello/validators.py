from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator


def valid_name(val):
    if not val.isalpha():
        raise ValidationError("Enter a valid name.")
    return "OK"

valid_skype = RegexValidator(r'^[0-9a-zA-Z_]*$', 'Enter a valid skype.')
valid_jabber = EmailValidator('Enter a valid jabber.')
