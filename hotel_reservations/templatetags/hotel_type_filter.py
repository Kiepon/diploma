from django import template

register = template.Library()

TYPE_TRANSLATIONS = {
    'hotel': 'Отель',
    'apartment': 'Апартаменты',
    'hostel': 'Хостел',
    'villa': 'Вилла',
    'resort': 'Курорт',
    'guesthouse': 'Гостевой дом',
    'motel': 'Мотель',
}

@register.filter(name='translate_property_type')
def translate_property_type(property_type):
    return TYPE_TRANSLATIONS.get(property_type.lower(), property_type)