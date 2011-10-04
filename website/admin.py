from django.contrib import admin

from website.models import Project, Member, News, BlogPost, Tag

admin.site.register(Project)
admin.site.register(Member)
admin.site.register(News)
admin.site.register(BlogPost)
admin.site.register(Tag)

# Include this here for now

from django.contrib import databrowse

databrowse.site.register(Project)
databrowse.site.register(Member)
databrowse.site.register(News)
databrowse.site.register(BlogPost)
databrowse.site.register(Tag)
