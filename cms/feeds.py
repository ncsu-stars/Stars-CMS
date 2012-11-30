from django.contrib.syndication.views import Feed, FeedDoesNotExist
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from cms.models import Member, BlogPost

class UserBlogFeed(Feed):

    description_template = "blogs/blog_rss.html"

    def get_object(self, request, **kwargs):
        return get_object_or_404(Member, pk=kwargs.get('pk', None))

    def title(self, obj):
        return "STARS Blog: " + obj.user.first_name + " " + obj.user.last_name

    def link(self, obj):
        return reverse("cms:blog_url", kwargs={'pk': obj.pk})

    def description(self, obj):
        return ""

    def items(self, obj):
        return BlogPost.objects.filter(author=obj).order_by('-date')[:30]

    def item_title(self, item):
        return item.title
