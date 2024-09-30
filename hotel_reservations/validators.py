from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def date_validator(value):
    if value < datetime.today().date():
        raise ValidationError(
            _('Дата должна быть больше либо равна текущей дате'),
            params={'value': value},
        )