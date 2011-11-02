from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
from django.contrib import databrowse

admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('cms.urls', namespace='cms')),
    (r'^admin/', include(admin.site.urls)),
    (r'^databrowse/(.*)', databrowse.site.root),

)

urlpatterns += staticfiles_urlpatterns()
