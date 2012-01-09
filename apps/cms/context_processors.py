from cms.models import Page

def pages(request):
    return {'pages': Page.objects.filter(pub_menu=True).order_by('title')}
