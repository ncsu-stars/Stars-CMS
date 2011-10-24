from django.contrib import admin

from website.models import Project, Member, News, BlogPost, Tag

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'members',)
    list_filter = ('title', 'members',)

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date')
    list_filter = ('author', 'date')

class MemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'classification')
    list_filter = ('group', 'classification')

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'date')
    list_filter = ('title', 'slug', 'date')

admin.site.register(Project, ProjectAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Tag)
