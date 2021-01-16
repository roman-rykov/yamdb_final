from rest_framework.exceptions import ValidationError


def validate_uniqueness(queryset, message=None, **kwargs):
    if message is None:
        message = 'object must be unique'
    if queryset.filter(**kwargs).exists():
        raise ValidationError({'non_field_errors': [message]})
