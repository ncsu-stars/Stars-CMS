import floppyforms

from django import forms
from django.forms import ModelForm, ModelChoiceField
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from website.models import Member, Project, BlogPost, Tag

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
	tags2 = forms.CharField(max_length=255, label="Tags")
	
	class Meta:
		model = BlogPost
		exclude = ('author','tags')

	def __init__(self, *args, **kwargs):
		instance = kwargs.get('instance', None)
		# See if we are editing an existing Blog. If not, there is nothing
		# to be done.
		if instance and instance.pk:
			taglist = Tag.objects.filter(blogpost=instance).values_list('name', flat=True)
			self.base_fields['tags2'].initial = ','.join(map(str, taglist))

		super(BlogForm, self).__init__(*args, **kwargs)

	def save(self, *args, **kwargs):       
		commit = kwargs.get('commit', True)        
		instance = super(BlogForm, self).save(*args, **kwargs)
		
		def save_m2m():
			taglist = self.cleaned_data['tags2'].split(",")
			instance.tags.clear()
			for t in taglist:
				tag = Tag.objects.get_or_create(name=t)[0]
				instance.tags.add(tag)

		if commit:
			save_m2m()
		else:
			self.save_m2m = func_concat(self.save_m2m, save_m2m)

		return instance
