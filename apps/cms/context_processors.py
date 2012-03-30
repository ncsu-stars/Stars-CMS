from cms.models import Page, Member, Project

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
    return {}
