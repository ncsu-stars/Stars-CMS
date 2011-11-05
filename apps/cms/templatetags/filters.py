from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode

import re
import calendar

register = template.Library()

@register.filter
@stringfilter
def stripjs(value):
    stripped = re.sub(r'<script(?:\s[^>]*)?(>(?:.(?!/script>))*</script>|/>)', \
                      '', force_unicode(value), flags=re.S)
    return mark_safe(stripped)

@register.filter
def logged_in(user):
    if user is None or user.id is None:
        return False

    return user.id != -1

# ref: http://stackoverflow.com/questions/7385751/how-to-display-month-name-by-number
@register.filter
def month_name(month_number):
    return calendar.month_name[month_number]
