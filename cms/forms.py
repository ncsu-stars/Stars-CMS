from django import forms
from django.conf import settings
from django.forms import ModelForm, ModelChoiceField
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from cms.models import Member, Project, ProjectMember, BlogPost, Tag, Page, Sponsor

class MemberForm(ModelForm):
    class Meta:
        model = Member
        exclude = ('user', 'status')

class MemberAdminForm(ModelForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    unity_id = forms.CharField(max_length=8, required=True, label='Unity ID')
    email = forms.EmailField(required=True)

    class Meta:
        model = Member
        fields = ('unity_id', 'first_name', 'last_name', 'email', 'group', 'classification',)

class ProjectAdminForm(ModelForm):
    members = Member.get_possible_project_members()

    coordinators = forms.ModelMultipleChoiceField(queryset=members)

    class Meta:
        model = Project
        fields = ('title', 'coordinators',)

class ProjectForm(ModelForm):
    members = forms.ModelMultipleChoiceField(queryset=Member.get_possible_project_members())

    class Meta:
        model = Project
        exclude = ('status','year')

    # special handling of ManyToMany members field
    # ref: http://stackoverflow.com/questions/387686/what-are-the-steps-to-make-a-modelform-work-with-a-manytomany-relationship-with
    def save(self, commit=True):
        project = super(ModelForm, self).save(commit=False)
        # save the regular fields
        project.save()

        # create ProjectMember instances for members listed in form that aren't added to Project yet
        for member in self.cleaned_data.get('members', []):
            try:
                project.members.get(pk=member.pk)
            except Member.DoesNotExist:
                project_member = ProjectMember(project=project, member=member, is_coordinator=False)
                project_member.save()
                #print 'add', project_member.member.user.get_full_name()

        # delete ProjectMember instances for members listed in Project but not in form
        for member in project.members.all():
            if not member in self.cleaned_data.get('members', []):
                project.projectmember_set.get(member__pk=member.pk).delete()
                #print 'delete', member.user.get_full_name()

        return project

class BlogForm(ModelForm):
    class Meta:
        model = BlogPost
        exclude = ('author',)

class PageForm(ModelForm):
    class Meta:
        model = Page

class SponsorForm(ModelForm):
    class Meta:
        model = Sponsor