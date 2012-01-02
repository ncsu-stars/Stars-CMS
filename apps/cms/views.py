from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseNotAllowed, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, TemplateView
from django.shortcuts import get_object_or_404

from datetime import datetime

from cms.models import Member, News, Page, Project, ProjectMember, BlogPost, Tag
from cms.forms import MemberForm, ProjectForm, BlogForm, MemberAdminForm, ProjectAdminForm

from cms import signals
from cms import academic_year
from cms import permissions

import time

class JSONResponseMixin(object):
    def get_json_response(self, json, **kwargs):
        return HttpResponse(json, content_type='application/json', **kwargs)

    def convert_to_json(self, context):
        return simplejson.dumps(context)

    def render_to_response(self, context):
        return self.get_json_response(self.convert_to_json(context))

class HomepageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        context['blog_posts'] = BlogPost.objects.all().order_by('-date')[:5]
        context['SPONSOR_LOGO_URL'] = settings.SPONSOR_LOGO_URL
        context['sponsors'] = settings.SPONSORS

        return context

class ProfileView(DetailView):
    model = Member
    template_name = 'members/profile.html'
    context_object_name = 'member'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)

       # NOTE: "year" is a field lookup type so must use "year__exact" instead
        project_members = ProjectMember.objects.filter(member__pk=self.kwargs.get('pk', None)).order_by('-project__year')
        context['project_groups'] = [ {'year': x, 'project_members': project_members.filter(project__year__exact=x).order_by('project__title') } for x in project_members.values_list('project__year', flat=True).distinct() ]

        context['recent_blogs'] = BlogPost.objects.filter(author__pk=self.kwargs.get('pk', None)).order_by('-date')[:3]

        return context

class EditProfileView(UpdateView):
    model = Member
    form_class = MemberForm
    template_name = 'members/edit_profile.html'

    def render_to_response(self, context):
        if permissions.can_user_edit_member(self.request.user, context['member']):
            return UpdateView.render_to_response(self, context)
        else:
            return HttpResponseForbidden('You do not have permission to edit this profile.')

class MembersView(ListView):
    model = Member
    template_name = 'members/members.html'
    context_object_name = 'members'

    def get_context_data(self, **kwargs):
        context = super(MembersView, self).get_context_data(**kwargs)

        # NOTE: "year" is a field lookup type so must use "year__exact" instead
        project_members = ProjectMember.objects.filter(project__year__exact=self.kwargs.get('year', settings.CURRENT_YEAR))
        context['members'] = Member.objects.filter(pk__in=project_members.values_list('member')).order_by('user__first_name', 'user__last_name').distinct()

        context['project_member_groups'] = [ {'group': x[1], 'members': Member.objects.filter(pk__in=project_members.filter(member__group=x[0]).values_list('member')).distinct().order_by('user__first_name', 'user__last_name')} for x in Member.GROUP_CHOICES ]
        context['project_member_groups'] += [ {'group': 'Volunteer', 'project_members': project_members.filter(member=None).order_by('volunteer_name')} ]

        context['year'] = self.kwargs.get('year', settings.CURRENT_YEAR)
        next_year = int(context['year']) + 1
        context['year2'] = next_year
        prev_year = int(context['year']) - 1

        if Project.objects.filter(year=next_year).count() > 0:
            context['next_year'] = next_year
            context['next_year2'] = next_year + 1
        if Project.objects.filter(year=prev_year).count() > 0:
            context['prev_year'] = prev_year
            context['prev_year2'] = prev_year + 1

        return context

    def render_to_response(self, context):
        # check for "year" in kwargs to avoid redirect loop when current year has no data
        if len(context['members']) == 0 and 'year' in self.kwargs:
            return HttpResponseRedirect(reverse('cms:members_url'))
        else:
            return super(MembersView, self).render_to_response(context)

class NewsView(ListView):
    model = News
    template_name = 'news/news.html'
    context_object_name = 'news_list'

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/article.html'
    context_object_name = 'news'

class PageDetailView(DetailView):
    model = Page
    template_name = 'pages/page.html'
    context_object_name = 'page'

class ProjectView(ListView):
    model = Project
    template_name = 'projects/projects.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(year=self.kwargs.get('year', settings.CURRENT_YEAR)).order_by('title')

    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs)

        context['project_groups'] = [ {'group': x[1], 'projects': context['projects'].filter(category=x[0])} for x in Project.CATEGORY_CHOICES ]

        context['year'] = self.kwargs.get('year', settings.CURRENT_YEAR)
        next_year = int(context['year']) + 1
        context['year2'] = next_year
        prev_year = int(context['year']) - 1

        if Project.objects.filter(year=next_year).count() > 0:
            context['next_year'] = next_year
            context['next_year2'] = next_year + 1
        if Project.objects.filter(year=prev_year).count() > 0:
            context['prev_year'] = prev_year
            context['prev_year2'] = prev_year + 1

        return context

    def render_to_response(self, context):
        # check for "year" in kwargs to avoid redirect loop when current year has no data
        if len(context['projects']) == 0 and 'year' in self.kwargs:
            return HttpResponseRedirect(reverse('cms:projects_url'))
        else:
            return super(ProjectView, self).render_to_response(context)

class EditProjectView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/edit_project.html'

    def render_to_response(self, context):
        if permissions.can_user_edit_project(self.request.user, context['project']):
            return UpdateView.render_to_response(self, context)
        else:
            return HttpResponseForbidden('You do not have permission to edit this project.')

class BlogsYearView(ListView):
    model = BlogPost
    template_name = 'blogs/blogs_year.html'
    context_object_name = 'blog_posts'
    paginate_by = 25

    def get_queryset(self):
        return BlogPost.objects.by_academic_year(self.kwargs.get('year', settings.CURRENT_YEAR)).order_by('date')

    def get_context_data(self, **kwargs):
        context = super(BlogsYearView, self).get_context_data(**kwargs)

        context['year'] = int(self.kwargs.get('year', settings.CURRENT_YEAR))
        next_year = context['year'] + 1
        context['year2'] = next_year
        prev_year = context['year'] - 1

        context['months'] = context['blog_posts'].dates('date', 'month', 'ASC')

        if BlogPost.objects.by_academic_year(next_year).count() > 0:
            context['next_year'] = next_year
            context['next_year2'] = next_year + 1
        if BlogPost.objects.by_academic_year(prev_year).count() > 0:
            context['prev_year'] = prev_year
            context['prev_year2'] = prev_year + 1

        return context

    def render_to_response(self, context):
        # check for "year" in kwargs to avoid redirect loop when current year has no data
        if len(context['blog_posts']) == 0 and 'year' in self.kwargs:
            return HttpResponseRedirect(reverse('cms:blogs_url'))
        else:
            return super(BlogsYearView, self).render_to_response(context)

class BlogsMonthView(ListView):
    model = BlogPost
    template_name = 'blogs/blogs_month.html'
    context_object_name = 'blog_posts'
    paginate_by = 25

    def get_queryset(self):
        return BlogPost.objects.filter(date__year=self.kwargs.get('year', settings.CURRENT_YEAR)).filter(date__month=self.kwargs.get('month', time.localtime().tm_mon)).order_by('date')

    def get_context_data(self, **kwargs):
        context = super(BlogsMonthView, self).get_context_data(**kwargs)

        year = int(self.kwargs.get('year', settings.CURRENT_YEAR))
        month = int(self.kwargs.get('month', time.localtime().tm_mon))

        context['year'] = year
        context['month'] = month

        context['next_month'] = (month + 0) % 12 + 1
        context['prev_month'] = (month - 2) % 12 + 1

        context['next_year'] = [ year, year + 1 ][month == 12]
        context['prev_year'] = [ year, year - 1 ][month == 1]

        return context

class BlogView(ListView):
    template_name = 'blogs/blogs.html'
    context_object_name = 'blog_posts'

    def get_queryset(self):
        return BlogPost.objects.filter(author__pk=self.kwargs.get('pk', None))

    def get_context_data(self, **kwargs):
        context = super(BlogView, self).get_context_data(**kwargs)
        context['member'] = get_object_or_404(Member, pk=self.kwargs.get('pk', None))

        return context

    #def render_to_response(self, context):
    #    return ListView.render_to_response(self, context)

class BlogPostView(DetailView):
    model = BlogPost
    template_name = 'blogs/blog_post.html'

    def get_context_data(self, **kwargs):
        context = super(BlogPostView, self).get_context_data(**kwargs)
        context['member'] = get_object_or_404(Member, pk=self.kwargs.get('pk', None))
        context['blog'] = get_object_or_404(BlogPost, pk=self.kwargs.get('blog_pk', None), author__pk=context['member'].pk)

        return context

class AddBlogView(CreateView):
    model = BlogPost
    form_class = BlogForm
    template_name = 'blogs/add_blog.html'
    object = None

    def dispatch(self, request, *args, **kwargs):
        member = get_object_or_404(Member, pk=kwargs.get('pk', None))
        if permissions.can_user_post_as_member(request.user, member):
            return super(AddBlogView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden('You do not have permission to post as that user.')

    def post(self, request, *args, **kwargs):
        member = get_object_or_404(Member, pk=self.kwargs.get('pk', None))
        form = BlogForm(request.POST)

        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.author = member
            self.object.save()
            form.save_m2m()
            return HttpResponseRedirect(self.object.get_absolute_url())
        else:
            return self.render_to_response(self.get_context_data(form=form, member=member))

    def get(self, request, *args, **kwargs):
        member = get_object_or_404(Member, pk=self.kwargs.get('pk', None))
        return self.render_to_response(self.get_context_data(form=BlogForm(), member=member))

class EditBlogView(UpdateView):
    model = BlogPost
    form_class = BlogForm
    template_name = 'blogs/edit_blog.html'
    context_object_name = 'blog'

    def get_object(self, **kwargs):
        return get_object_or_404(BlogPost, pk=self.kwargs.get('blog_pk', None), author__pk=self.kwargs.get('pk', None))

    def get_context_data(self, **kwargs):
        context = super(EditBlogView, self).get_context_data(**kwargs)
        context['member'] = get_object_or_404(Member, pk=self.kwargs.get('pk', None))
        #context['blog'] = get_object_or_404(BlogPost, pk=self.kwargs.get('blog_pk', None), author__pk=context['member'].pk)

        return context

    def render_to_response(self, context):
        if permissions.can_user_edit_blogpost(self.request.user, context['blog']):
            return UpdateView.render_to_response(self, context)
        else:
            return HttpResponseForbidden('You do not have permission to edit this blog post.')

class TagCloudView(JSONResponseMixin, View):
    def post(self, request, *args, **kwargs):
        tag_name = request.POST.get('tag', None)
        if tag_name is not None:
            blog_post = get_object_or_404(BlogPost, pk=request.POST.get(['blog_id'], None), author__pk=request.POST.get(['member_id'], None))
            tag = Tag.objects.get_or_create(name=tag_name)

        return HttpResponse()

    def get(self, request, *args, **kwargs):
        tags = Tag.objects.all()
        response = {}

        for tag in tags:
            response[tag.name] = BlogPost.objects.filter(tags__name=tag.name).count()

        return JSONResponseMixin.render_to_response(self, response)

class CreateProjectView(CreateView):
    model = Project
    form_class = ProjectAdminForm
    template_name = 'projects/create.html'

    def get_context_data(self, **kwargs):
        return kwargs

    def render_to_response(self, context):
        if permissions.can_user_create_project(self.request.user):
            return CreateView.render_to_response(self, context)
        else:
            return HttpResponseForbidden('You do not have permission to access this page.')

    def post(self, request, *args, **kwargs):
        if permissions.can_user_create_project(self.request.user):
            form = ProjectAdminForm(request.POST)

            if form.is_valid():
                project = form.save(commit=False)
                project.year = settings.CURRENT_YEAR
                project.status = 0 # Empty, so a coordinator can fill out the project information
                project.save()

                signals.assign_coordinators.send(sender=None, project=project, members=form.cleaned_data['coordinators'])

                return HttpResponseRedirect(reverse('cms:projects_url'))
            else:
                self.render_to_response(self.get_context_data(form=form))
        else:
            return HttpResponseForbidden('You do not have permission to access this page.')

class CreateMemberView(CreateView):
    model = Member
    form_class = MemberAdminForm
    template_name = 'members/create.html'

    def get_context_data(self, **kwargs):
        return kwargs

    def render_to_response(self, context):
        if permissions.can_user_create_member(self.request.user):
            return CreateView.render_to_response(self, context)
        else:
            return HttpResponseForbidden('You do not have permission to access this page.')

    def post(self, request, *args, **kwargs):
        if permissions.can_user_create_member(self.request.user):
            form = MemberAdminForm(request.POST)

            if form.is_valid():
                unity_id = request.POST['unity_id']
                email = request.POST['email']
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                group = request.POST['group']
                classification = request.POST['classification']

                user = User.objects.create(username=unity_id, email=email, first_name=first_name, last_name=last_name)
                member, project_member = signals.create_profile.send(sender=None, user=user, group=group, classification=classification)

                return HttpResponseRedirect(reverse('cms:members_url'))
            else:
                self.render_to_response(self.get_context_data(form=form))
        else:
            return HttpResponseForbidden('You do not have permission to access this page.')

class ActivateMemberView(UpdateView):
    model = Member
    form_class = MemberForm
    template_name = 'members/activate.html'

    def get_object(self, queryset):
        pass

    def post(self, request, *args, **kwargs):
        pass

    def render_to_response(self, context):
        return TemplateView.render_to_response(self, context)
