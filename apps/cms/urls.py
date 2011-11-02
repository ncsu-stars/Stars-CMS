from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from cms.views import HomepageView, ProfileView, NewsView, NewsDetailView, PageDetailView
from cms.views import ProjectView, MembersView, EditProfileView, EditProjectView, BlogView
from cms.views import BlogPostView, AddBlogView, EditBlogView, TagCloudView

urlpatterns = (
    url(r'^$', HomepageView.as_view(), name='homepage_url'),
    url(r'^news/$', NewsView.as_view(), name='news_url'),
    url(r'^news/(?P<pk>\d+)/(?P<slug>\w+)/$', NewsDetailView.as_view(), name='news_detail_url'),
    url(r'^page/(?P<slug>\w+)/$', PageDetailView.as_view(), name='page_url'),
)

urlpatterns += (
    url(r'^projects/$', ProjectView.as_view(), name='projects_url'),
    url(r'^projects/(?P<year>\d+)/$', ProjectView.as_view(), name='projects_year_url'),
    url(r'^project/(?P<pk>\d+)/edit/$', EditProjectView.as_view(), name='edit_project_url'),
    #url(r'^blogs/$', BlogView.as_view(), name='blogs_url'),
    #url(r'^blogs/(?P<year>\d+)/$', ProjectView.as_view(), name='blogs_year_url'),
    #url(r'^blogs/(?P<year>\d+)/(?P<month>\d+)/$', EditProjectView.as_view(), name='blogs_month_url'),
)

urlpatterns += (
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login_url'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}, name='logout_url'),
    url(r'^members/$', MembersView.as_view(), name='members_url'),
    url(r'^members/(?P<year>\d+)/$', MembersView.as_view(), name='members_year_url'),
    url(r'^member/(?P<pk>\d+)/$', ProfileView.as_view(), name='profile_url'),
    url(r'^member/(?P<pk>\d+)/edit/$', EditProfileView.as_view(), name='edit_profile_url'),
)

urlpatterns += (
    url(r'^member/(?P<pk>\d+)/blog/$', BlogView.as_view(), name='blog_url'),
    url(r'^member/(?P<pk>\d+)/blog/(?P<blog_pk>\d+)/$', BlogPostView.as_view(), name='blog_post_url'),
    url(r'^member/(?P<pk>\d+)/blog/add/$', AddBlogView.as_view(), name='add_blog_url'),
    url(r'^member/(?P<pk>\d+)/blog/(?P<blog_pk>\d+)/edit/$', EditBlogView.as_view(), name='edit_blog_url'),
)

urlpatterns += (
    url(r'^tags/$', TagCloudView.as_view(), name='tag_cloud_url'),
)

urlpatterns += (
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
