import re
import calendar

from django import template
from django.conf import settings
from django.contrib.auth.models import User
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode

from cms import permissions

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
	return permissions.is_user_slc_leader(user)

@register.filter
def can_edit_project(user, project):
	return permissions.can_user_edit_project(user, project)

@register.filter
def can_edit_member(user, member):
	return permissions.can_user_edit_member(user, member)

@register.filter
def can_edit_blogpost(user, blogpost):
	return permissions.can_user_edit_blogpost(user, blogpost)

@register.filter
def is_project_coordinator(member, project):
	return project.is_member_coordinator(member)

# ref: http://stackoverflow.com/questions/7385751/how-to-display-month-name-by-number
@register.filter
def month_name(month_number):
    return calendar.month_name[month_number]
