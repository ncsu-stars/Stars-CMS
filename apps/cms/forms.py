import floppyforms

from django import forms
from django.conf import settings
from django.forms import ModelForm, ModelChoiceField
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from cms.models import Member, Project, ProjectMember, BlogPost, Tag

class MemberForm(ModelForm):
    class Meta:
        model = Member
        exclude = ('user',)
        
class MemberAdminForm(ModelForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    unity_id = forms.CharField(max_length=8, required=True, label='Unity ID')
    email = forms.EmailField(required=True)
    
    class Meta:
        model = Member
        fields = ('first_name', 'last_name', 'email', 'unity_id', 'group', 'classification',)
        
class ProjectAdminForm(ModelForm):
    #members = Member.objects.filter(pk__in=ProjectMember.objects.filter(project__year__exact= \
    #    settings.CURRENT_YEAR).distinct().values_list('member')).order_by('user__first_name', 'user__last_name')
    members = Member.get_current_members()

    coordinators = forms.ModelMultipleChoiceField(queryset=members)

    class Meta:
        model = Project
        fields = ('title', 'coordinators',)

class ProjectForm(ModelForm):
    class Meta:
        model = Project

class BlogForm(ModelForm):
    class Meta:
        model = BlogPost
        exclude = ('author',)
