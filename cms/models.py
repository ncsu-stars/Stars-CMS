import hashlib

from django.db import models
from django.contrib.auth.models import User

from cms.managers import BlogPostManager
from cms.storage import OverwriteStorage

import os
from django.core.urlresolvers import reverse

MEMBER_IMAGE_FOLDER = 'member'
def make_member_image_name(instance, filename):
    if instance.pk is None:
        raise Exception('save Member instance before saving ImageField')
    return os.path.join(MEMBER_IMAGE_FOLDER, str(instance.pk) + os.path.splitext(filename)[1].lower())

PROJECT_IMAGE_FOLDER = 'project'
def make_project_image_name(instance, filename):
    if instance.pk is None:
        raise Exception('save Project instance before saving ImageField')
    return os.path.join(PROJECT_IMAGE_FOLDER, str(instance.pk) + os.path.splitext(filename)[1].lower())

SPONSOR_IMAGE_FOLDER = 'sponsor'
def make_sponsor_image_name(instance, filename):
    if instance.pk is None:
        raise Exception('save Sponsor instance before saving ImageField')
    return os.path.join(SPONSOR_IMAGE_FOLDER, str(instance.pk) + os.path.splitext(filename)[1].lower())

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
    homepage        = models.URLField(blank=True)
    blurb           = models.TextField(blank=True)
    image           = models.ImageField(upload_to=make_member_image_name, storage=OverwriteStorage(), blank=True)
    status          = models.IntegerField(choices=STATUS_CHOICES)
    #activation_key  = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return unicode(self.user.get_full_name())

    def get_absolute_url(self):
        return reverse('cms:profile_url', kwargs={'pk': self.pk})

    def generate_hashed_email(self):
        return hashlib.md5(self.user.email).hexdigest()

    def get_coordinated_projects(self):
        return Project.objects.filter(pk__in=ProjectMember.objects.filter(member__pk=self.pk, is_coordinator=True).values_list('project__pk', flat=True))

    @staticmethod
    def get_possible_project_members():
        # need to allow member one year old as well since activity status is predicated on project membership
	    # but you can't create a project for a new year without a project coordinator
        # hence, the one year offset avoids the chicken-and-the-egg problem
        #return Member.objects.filter(Q(status=Member.STATUS_ACTIVE) | Q(pk__in=ProjectMember.objects.filter(project__year__gte= \
        #    settings.CURRENT_YEAR-1).distinct().values_list('member'))).order_by('user__first_name', 'user__last_name')
        return Member.objects.exclude(status=Member.STATUS_ARCHIVED).order_by('user__first_name', 'user__last_name')

    class Meta:
        verbose_name        = 'member'
        verbose_name_plural = 'members'
        ordering            = ['user__first_name']

class Project(models.Model):
    STATUS_EMPTY    = 0 # this project is pending "creation" by coordinator
    STATUS_ACTIVE   = 1 # this project has been created and is editable by coordinators
    STATUS_ARCHIVED = 2 # this project has been archived and is frozen

    STATUS_CHOICES  = (
        (STATUS_EMPTY, u'Empty'),
        (STATUS_ACTIVE, u'Active'),
        (STATUS_ARCHIVED, u'Archived')
    )

    CATEGORY_OTHER          = 0
    CATEGORY_OUTREACH       = 1
    CATEGORY_RESEARCH       = 2
    CATEGORY_SERVICE        = 3
    CATEGORY_INTERNSHIP     = 4
    CATEGORY_ORGANIZATIONAL = 5

    CATEGORY_CHOICES = (
        (CATEGORY_OUTREACH, u'Outreach'),
        (CATEGORY_RESEARCH, u'Research'),
        (CATEGORY_SERVICE, u'Service'),
        (CATEGORY_INTERNSHIP, u'Internship'),
        (CATEGORY_ORGANIZATIONAL, u'Organizational'),
        (CATEGORY_OTHER, u'Other'),
    )

    title           = models.CharField(max_length=255)
    description     = models.TextField()
    image           = models.ImageField(upload_to=make_project_image_name, storage=OverwriteStorage(), blank=True)
    #active          = models.BooleanField(default=False)
    status          = models.IntegerField(choices=STATUS_CHOICES)
    category        = models.IntegerField(choices=CATEGORY_CHOICES, default=CATEGORY_OTHER)
    year            = models.IntegerField()
    members         = models.ManyToManyField(Member, through='ProjectMember')
    parent          = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return unicode('%s %d' % (self.title, self.year))

    def get_absolute_url(self):
        return reverse('cms:projects_year_pk_url', kwargs={'year': self.year, 'pk': self.pk})

    def is_member_coordinator(self, member):
        return ProjectMember.objects.filter(member__pk=member.pk, project__pk=self.pk, is_coordinator=True).count() != 0

    class Meta:
        verbose_name        = 'project'
        verbose_name_plural = 'projects'

class ProjectMember(models.Model):
    project         = models.ForeignKey(Project)
    member          = models.ForeignKey(Member, blank=True, null=True)
    role            = models.CharField(max_length=255, blank=True)
    volunteer_name  = models.CharField(max_length=255, blank=True)
    is_coordinator  = models.BooleanField()

    class Meta:
        ordering    = [ '-is_coordinator', 'member__user__first_name', 'volunteer_name' ]

    def is_volunteer(self):
        return self.member is None

    def get_full_name(self):
        if self.is_volunteer():
            return unicode(self.volunteer_name)
        else:
            return self.member.user.get_full_name()

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
    slug            = models.SlugField(max_length=100, unique=True)
    weight          = models.IntegerField(default=0)
    pub_front_page  = models.BooleanField(default=False, verbose_name='Publish on homepage')
    pub_menu        = models.BooleanField(default=False, verbose_name='Publish on top menu')

    def __unicode__(self):
        return unicode(self.title)

    def get_absolute_url(self):
        return reverse('cms:page_url', kwargs={'slug': self.slug})

class Tag(models.Model):
    name            = models.CharField(max_length=255)

    def __unicode__(self):
        return unicode(self.name)

class BlogPost(models.Model):
    author          = models.ForeignKey(Member)
    title           = models.CharField(max_length=255)
    date            = models.DateTimeField(auto_now_add=True)
    edit_date       = models.DateTimeField(auto_now=True)
    post            = models.TextField(help_text='HTML is allowed')
    tags            = models.ManyToManyField(Tag, blank=True, related_name='blogposts')

    objects         = BlogPostManager()

    def get_absolute_url(self):
        return reverse('cms:blog_post_url', kwargs={'pk': self.author.pk, 'blog_pk': self.pk})

    def __unicode__(self):
        return unicode('%s by %s' % (self.title, self.author))

    class Meta:
        verbose_name        = 'blog post'
        verbose_name_plural = 'blog posts'
        ordering            = ['-date']

class Sponsor(models.Model):
    name            = models.CharField(max_length=255)
    image           = models.ImageField(upload_to=make_sponsor_image_name, storage=OverwriteStorage(), blank=True)

    def __unicode__(self):
        return unicode(self.name)

    def get_absolute_url(self):
        return reverse('cms:sponsors_url')

    def save(self, **kwargs):
        img_tmp = self.image
        self.image = None
        super(Sponsor, self).save()
        self.image = img_tmp
        return super(Sponsor, self).save()

    class Meta:
        verbose_name        = 'sponsor'
        verbose_name_plural = 'sponsors'
