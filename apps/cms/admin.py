from django.contrib import admin

from cms.models import Project, Member, News, BlogPost, Tag, ProjectMember

class ProjectMemberInline(admin.StackedInline):
    model = ProjectMember
    fields = ( 'member', 'volunteer_name', 'role', 'is_coordinator', )

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'status')
    list_filter = ('year', 'status')
    ordering = ('-year', 'title', 'status')
    search_fields = ('title', 'description', 'members__member__user__last_name', 'members__member__user__first_name')
    inlines = [ ProjectMemberInline ]

class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'is_volunteer', 'is_coordinator', 'role', 'project', 'get_year')
    list_filter = ('project', 'project__year', 'is_coordinator', 'role')
    ordering = ('-project__year',)

    def get_year(self, project_member):
        return project_member.project.year

    def is_volunteer(self, project_member):
        return project_member.is_volunteer()
    is_volunteer.boolean = True

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date')
    list_filter = ('author', 'date')

class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'group', 'classification', 'status')
    list_filter = ('group', 'classification', 'status')
    ordering = ('user__last_name', 'user__first_name', 'group', 'status')
    search_fields = ('user__last_name', 'user__first_name')

    def name(self, member):
        return member.user.get_full_name()

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'date')
    list_filter = ('title', 'slug', 'date')

admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectMember, ProjectMemberAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Tag)
