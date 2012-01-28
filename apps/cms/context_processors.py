from cms.models import Page

def pages(request):
    return {'menu_pages': Page.objects.filter(pub_menu=True).order_by('weight')}
