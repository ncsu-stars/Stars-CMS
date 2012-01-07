from django.http import Http404, HttpResponseForbidden
from django.template import loader, RequestContext, TemplateDoesNotExist

class HttpResponseErrorToTemplate:
    def process_response(self, request, response):
        if response.status_code == 403:
            try:
                t = loader.get_template('403.html')
            except TemplateDoesNotExist:
                return response
            else:
                return HttpResponseForbidden(t.render(RequestContext(request, {'message': response.content})))
        else:
            return response
