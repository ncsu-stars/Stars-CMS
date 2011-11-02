import floppyforms

from django import forms
from django.forms import ModelForm, ModelChoiceField
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from cms.models import Member, Project, BlogPost, Tag

class MemberForm(ModelForm):
	class Meta:
		model = Member
		exclude = ('user',)

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
