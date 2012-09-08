from django.contrib.auth.models import User, Group
from cms.models import Member, Project, ProjectMember, BlogPost
from django.conf import settings

def is_user_slc_leader(user):
    if user is None or user.is_anonymous():
        return False
    else:
        return (user.get_full_name() in settings.SLC_LEADERS)

def can_user_create_project(user):
    # only the SLC leader can create projects through the main interface
    return is_user_slc_leader(user)

def can_user_edit_project(user, project):
    # only project coordinators (active/empty projects) and the SLC leader
    # can edit projects through the main interface
    # editing of archived projects is disallowed except for SLC leader
    if user.is_anonymous():
        return False

    if is_user_slc_leader(user):
        return True

    try:
        return (project.status != Project.STATUS_ARCHIVED) and project.is_member_coordinator(user.get_profile())
    except Member.DoesNotExist:
        return False

def can_user_delete_project(user, project):
    # only the SLC leader can delete projects through the main interface
    # project status is not checked since the SLC leader user overrides
    return is_user_slc_leader(user)

def can_user_demote_project_coordinators(user, project):
    # only the SLC leader can demote project coordinators through the main interface
    return is_user_slc_leader(user)

def can_user_create_member(user):
    # only the SLC leader can create members through the main interface
    return is_user_slc_leader(user)

def can_user_edit_member(user, member):
    # only the user that owns a member profile and the SLC leader can perform edits
    # through the main interface
    # but only if that member is not archived for normal users (strictly not necessary since inactive user cannot log in)
    return ((member.status != Member.STATUS_ARCHIVED) and (user == member.user)) or is_user_slc_leader(user)

def can_user_delete_member(user, member):
    # only the SLC leader can delete members through the main interface
    # member status is not checked since the SLC leader user overrides
    return is_user_slc_leader(user)


def can_user_archive_member(user, member):
    # only the SLC leader can delete members through the main interface
    # member status is not checked since the SLC leader user overrides
    return is_user_slc_leader(user)


def can_user_post_as_member(user, member):
    # only the user that owns a member profile can post to that member's blog
    # but only if that member is not archived for normal users (strictly not necessary since inactive user cannot log in)
    return ((member.status != Member.STATUS_ARCHIVED) and (user == member.user))

def can_user_edit_blogpost(user, blogpost):
    # only blogpost authors and the SLC leader can edit blogposts
    # through the main interface
    # but only if that member is not archived for normal users (strictly not necessary since inactive user cannot log in)
    return ((blogpost.author.status != Member.STATUS_ARCHIVED) and (user == blogpost.author.user)) or is_user_slc_leader(user)

def can_user_create_page(user):
    # only the SLC leader can create pages through the main interface
    return is_user_slc_leader(user)

def can_user_edit_page(user, page):
    # only the SLC leader can edit pages through the main interface
    return is_user_slc_leader(user)

def can_user_delete_page(user, page):
    # only the SLC leader can delete pages through the main interface
    return is_user_slc_leader(user)

