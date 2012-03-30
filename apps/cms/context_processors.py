from cms.models import Page, Member, Project, ProjectMember

def pages(request):
    return {'menu_pages': Page.objects.filter(pub_menu=True).order_by('weight')}

def member_empty(request):
    if not request.user.is_anonymous():
        try:
            member = request.user.get_profile()
        except Member.DoesNotExist:
            pass
        else:
            if member.status == Member.STATUS_EMPTY:
                return {'empty_profile': member}

    return {}

def project_empty(request):
    if not request.user.is_anonymous():
        try:
            member = request.user.get_profile()
        except Member.DoesNotExist:
            pass
        else:
            projects = Project.objects.filter(status=Project.STATUS_EMPTY, pk__in=member.projectmember_set.filter(is_coordinator=True).values_list('project', flat=True))
            if len(projects):
                return {'empty_projects': projects}

    return {}
