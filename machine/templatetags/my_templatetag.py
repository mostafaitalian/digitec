from django.utils.safestring import mark_safe
from django.template import Library
import json

register  = Library()

# @register.filter(name='js',is_safe=True)

# def js(obj):
    
#     return mark_safe(json.dumps(obj))

# return all calls for certain machine except the call with notify

@register.filter(name='matched')
def matched(obj, notify):
    calls = obj.machine.calls.exclude(notification_number=notify)
    return calls

    
@register.filter(name='get_data')
def get_data(obj):
    pass