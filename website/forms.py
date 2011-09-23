import floppyforms

from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from website.models import Member, Project, BlogPost

class MemberForm(ModelForm):
	class Meta:
		model = Member
		exclude = ('user',)

class ProjectForm(ModelForm):
	class Meta:
		model = Project

class BlogForm(ModelForm):
	class Meta:
		model = BlogPost
		exclude = ('author',)