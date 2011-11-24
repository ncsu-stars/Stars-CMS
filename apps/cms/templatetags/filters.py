from django import template
from django.conf import settings
from django.contrib.auth.models import User
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

@register.filter
def is_slc_leader(user):
	slc_leader = User.objects.get(first_name=settings.SLC_LEADER.split(' ')[0], last_name=settings.SLC_LEADER.split(' ')[1])

	return user == slc_leader

@register.filter
def is_project_coordinator(member, project):
	return project.is_member_coordinator(member)

# ref: http://stackoverflow.com/questions/7385751/how-to-display-month-name-by-number
@register.filter
def month_name(month_number):
    return calendar.month_name[month_number]
