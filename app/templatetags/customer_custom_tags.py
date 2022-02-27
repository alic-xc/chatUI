from math import floor
from django.template import Library
import datetime


register = Library()


@register.filter(expects_localtime=True)
def string_to_date(value):
    try:
        if not value:
            return 'N/A'

        return datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
    except Exception:
        return datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')


@register.filter(expects_localtime=True)
def string_to_date_object(value):
    try:

        return datetime.datetime.strptime(value, '%Y-%m-%d').date()
    except:
        if value != 'N/A' and value != '':
            # return "%s" % value
            return value.date()
        else:
            return ''