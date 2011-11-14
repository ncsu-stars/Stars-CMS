import floppyforms

from django import forms
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
    coordinator = forms.ModelMultipleChoiceField(queryset=ProjectMember.objects.all())

    class Meta:
        model = Project
        fields = ('title', 'year', 'coordinator',)

class ProjectForm(ModelForm):
	class Meta:
		model = Project

def func_concat(old_func, new_func):
    def function():
        old_func()
        new_func()
    return function

class BlogForm(ModelForm):
	class Meta:
		model = BlogPost
		exclude = ('author',)
