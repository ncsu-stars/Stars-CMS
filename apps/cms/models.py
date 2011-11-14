from django.db import models
from django.conf import settings
from django.db.models import signals
from django.contrib.auth.models import User
import django.contrib.localflavor.us.us_states as states

from cms.managers import BlogPostManager

class Project(models.Model):
    STATUS_EMPTY    = 0 # this project is pending "creation" by coordinator
    STATUS_ACTIVE   = 1 # this project has been created and is editable by coordinators
    STATUS_ARCHIVED = 2 # this project has been archived and is frozen

    STATUS_CHOICES  = (
        (STATUS_EMPTY, u'Empty'),
        (STATUS_ACTIVE, u'Active'),
        (STATUS_ARCHIVED, u'Archived')
    )

    title           = models.CharField(max_length=255)
    description     = models.TextField()
    image           = models.ImageField(upload_to='project_images')
    #active          = models.BooleanField(default=False)
    status          = models.IntegerField(choices=STATUS_CHOICES)
    year            = models.IntegerField()

    def __unicode__(self):
        return unicode('%s %d' % (self.title, self.year))

    @models.permalink
    def get_absolute_url(self):
        return ('cms:projects_url', (), {})

    def is_member_coordinator(self, member):
        return ProjectMember.objects.filter(member__pk=member.pk, project__pk=self.pk, is_coordinator=True).count() != 0

    class Meta:
        verbose_name        = 'project'
        verbose_name_plural = 'projects'

class Member(models.Model):
    GROUP_CHOICES = (
        (u'graduate', u'Graduate'),
        (u'undergraduate', u'Undergraduate'),
        (u'faculty', u'Faculty')
    )

    CLASS_CHOICES = (
        (u'freshman', u'Freshman'),
        (u'sophomore', u'Sophomore'),
        (u'junior', u'Junior'),
        (u'senior', u'Senior')
    )

    STATUS_EMPTY    = 0 # this member is pending "creation" by its owner
    STATUS_ACTIVE   = 1 # this member has been created
    STATUS_ARCHIVED = 2 # this member has been archived and is frozen

    STATUS_CHOICES  = (
        (STATUS_EMPTY, u'Empty'),
        (STATUS_ACTIVE, u'Active'),
        (STATUS_ARCHIVED, u'Archived')
    )

    user            = models.ForeignKey(User, related_name='profile', unique=True)
    group           = models.CharField(max_length=255, choices=GROUP_CHOICES)
    classification  = models.CharField(max_length=255, choices=CLASS_CHOICES, blank=True)
    hometown        = models.CharField(max_length=255, blank=True)
    interests       = models.TextField(blank=True)
    homepage        = models.URLField(verify_exists=False, blank=True)
    blurb           = models.TextField(blank=True)
    image           = models.ImageField(upload_to='user_images', blank=True)
    status          = models.IntegerField(choices=STATUS_CHOICES)

    def __unicode__(self):
        return unicode(self.user.get_full_name())

    @models.permalink
    def get_absolute_url(self):
        return ('cms:profile_url', (self.pk,), {})

    def get_coordinated_projects(self):
        return Project.objects.filter(pk__in=ProjectMember.objects.filter(member__pk=self.pk, is_coordinator=True).values_list('project__pk', flat=True))
    
    class Meta:
        verbose_name        = 'member'
        verbose_name_plural = 'members'
        ordering            = ['user__last_name']

class ProjectMember(models.Model):
    project         = models.ForeignKey(Project, related_name='members')
    member          = models.ForeignKey(Member, blank=True, related_name='project_members')
    role            = models.CharField(max_length=255, blank=True)
    volunteer_name  = models.CharField(max_length=255, blank=True)
    is_coordinator  = models.BooleanField()

    def is_volunteer(self):
        return self.member is None

    def get_full_name(self):
        if self.is_volunteer:
            return self.member.user.get_full_name()
        else:
            return unicode(self.volunteer_name)

    def __unicode__(self):
        if self.role:
            return unicode('%s (%s)' % (self.get_full_name(), self.role))
        else:
            return self.get_full_name()

class News(models.Model):
    title           = models.CharField(max_length=255)
    description     = models.TextField(max_length=200)
    content         = models.TextField()
    date            = models.DateTimeField()
    slug            = models.SlugField(max_length=100)

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        verbose_name        = 'news'
        verbose_name_plural = 'news'

class Page(models.Model):
    title           = models.CharField(max_length=255)
    content         = models.TextField()
    slug            = models.SlugField(max_length=100)
    pub_front_page  = models.BooleanField(default=False)
    pub_menu        = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.title)

class Tag(models.Model):
    name            = models.CharField(max_length=255)

    def __unicode__(self):
        return unicode(self.name)

class BlogPost(models.Model):
    author          = models.ForeignKey(Member)
    title           = models.CharField(max_length=255)
    date            = models.DateTimeField()
    post            = models.TextField()
    tags            = models.ManyToManyField(Tag, blank=True, related_name='blogposts')

    objects         = BlogPostManager()

    @models.permalink
    def get_absolute_url(self):
        return ('cms:blog_post_url', (), {'pk': self.author.pk, 'blog_pk': self.pk})

    def __unicode__(self):
        return unicode('%s by %s' % (self.title, self.author))

    class Meta:
        verbose_name        = 'blog post'
        verbose_name_plural = 'blog posts'
        ordering            = ['-date']
