from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from cms.views import HomepageView, ProfileView, NewsView, NewsDetailView, PageDetailView
from cms.views import ProjectView, MembersView, EditProfileView, EditProjectView, BlogView
from cms.views import BlogPostView, AddBlogView, EditBlogView, TagCloudView, BlogsYearView
from cms.views import BlogsMonthView, CreateProjectView, CreateMemberView, ActivateMemberView
from cms.views import SponsorView, CreateSponsorView, DeleteSponsorView
from cms.views import DeleteProjectView, CreatePageView, EditPageView, PageAllView, ArchiveMemberView, DeleteMemberView, ReactivateMemberView, DeletePageView
from cms.feeds import UserBlogFeed, BlogFeed

urlpatterns = (
    url(r'^$', HomepageView.as_view(), name='homepage_url'),
    url(r'^news/$', NewsView.as_view(), name='news_url'),
    url(r'^news/(?P<pk>\d+)/(?P<slug>\w+)/$', NewsDetailView.as_view(), name='news_detail_url'),
)

urlpatterns += (
    url(r'^page/create/$', CreatePageView.as_view(), name='create_page_url'),
    url(r'^page/s/(?P<slug>\w+)/$', PageDetailView.as_view(), name='page_url'),
    url(r'^page/(?P<pk>\d+)/edit/$', EditPageView.as_view(), name='edit_page_url'),
    url(r'^page/(?P<pk>\d+)/delete/$', DeletePageView.as_view(), name='delete_page_url'),
    url(r'^page/all/$', PageAllView.as_view(), name='pages_all_url'),
)

urlpatterns += (
    url(r'^project/create/$', CreateProjectView.as_view(), name='create_project_url'),
    url(r'^project/all/$', ProjectView.as_view(), name='projects_url'),
    url(r'^project/all/(?P<year>\d+)/$', ProjectView.as_view(), name='projects_year_url'),
    url(r'^project/(?P<pk>\d+)/edit/$', EditProjectView.as_view(), name='edit_project_url'),
    url(r'^project/(?P<pk>\d+)/delete/$', DeleteProjectView.as_view(), name='delete_project_url'),
)

urlpatterns += (
    url(r'^blog/all/$', BlogsYearView.as_view(), name='blogs_url'),
    url(r'^blog/all/(?P<year>\d+)/$', BlogsYearView.as_view(), name='blogs_year_url'),
    url(r'^blog/all/(?P<year>\d+)/(?P<month>\d+)/$', BlogsMonthView.as_view(), name='blogs_month_url'),
    url(r'^blog/rss/$', BlogFeed(), name='blogs_rss_url'),
)

urlpatterns += (
    url(r'^login/$', 'ncsu.wrap.views.login', {'template_name': 'login.html'}, name='login_url'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}, name='logout_url'),
)

urlpatterns += (
    url(r'^people/create/$', CreateMemberView.as_view(), name='create_member_url'),
    url(r'^people/activate/(?P<key>\w+)/$', ActivateMemberView.as_view(), name='activate_member_url'),
    url(r'^people/(?P<pk>\w+)/reactivate/$', ReactivateMemberView.as_view(), name='reactivate_member_url'),
    url(r'^people/all/$', MembersView.as_view(), name='members_url'),
    url(r'^people/all/(?P<year>\d+)/$', MembersView.as_view(), name='members_year_url'),
    url(r'^people/(?P<pk>\d+)/$', ProfileView.as_view(), name='profile_url'),
    url(r'^people/(?P<pk>\d+)/edit/$', EditProfileView.as_view(), name='edit_profile_url'),
    url(r'^people/(?P<pk>\d+)/blog/$', BlogView.as_view(), name='blog_url'),
    url(r'^people/(?P<pk>\d+)/blog/(?P<blog_pk>\d+)/$', BlogPostView.as_view(), name='blog_post_url'),
    url(r'^people/(?P<pk>\d+)/blog/add/$', AddBlogView.as_view(), name='add_blog_url'),
    url(r'^people/(?P<pk>\d+)/blog/rss/$', UserBlogFeed(), name='blog_rss_url'),
    url(r'^people/(?P<pk>\d+)/blog/(?P<blog_pk>\d+)/edit/$', EditBlogView.as_view(), name='edit_blog_url'),
    url(r'^people/(?P<pk>\d+)/delete/$', DeleteMemberView.as_view(), name='delete_member_url'),
    url(r'^people/(?P<pk>\d+)/archive/$', ArchiveMemberView.as_view(), name='archive_member_url'),
)

urlpatterns += (
    url(r'^tags/$', TagCloudView.as_view(), name='tag_cloud_url'),
)

urlpatterns += (
    url(r'^sponsors/$', SponsorView.as_view(), name='sponsors_url'),
    url(r'^sponsors/create$', CreateSponsorView.as_view(), name='create_sponsor_url'),
    url(r'^sponsors/(?P<pk>\d+)/delete$', DeleteSponsorView.as_view(), name='delete_sponsor_url'),
)

if settings.DEBUG:
    urlpatterns += (
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
