from django.conf import settings
from django.dispatch import Signal, receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save, post_save
from django.contrib.sites.models import Site

from cms.models import Member, ProjectMember, Project

create_profile = Signal(providing_args=['user', 'group', 'classification'])
assign_coordinators = Signal(providing_args=['project', 'members'])

# Create a member profile and a project member profile
def create_profile_handler(sender, **kwargs):
    user = kwargs.get('user', None)
    group = kwargs.get('group', None)
    classification = kwargs.get('classification', None)
    
    member = Member(user=user, group=group, status=0, classification=classification)
    member.save()

    context = {
    	'name': member.user.get_full_name(),
    	'url': Site.objects.get_current().domain + reverse('cms:activate_member_url', kwargs={'key': member.generate_hashed_email()})
    }

    subject = 'Welcome to STARS'
    message = render_to_string('emails/new_member_email.txt', context)
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

    return (member, project_member,)

# Create project member profiles and send each coordinator an email
def assign_coordinators_handler(sender, **kwargs):
	members = kwargs.get('members', None)
	project = kwargs.get('project', None)

	for member in members:
		project_member = ProjectMember(member=member, project=project, is_coordinator=True, role='Coordinator')
		project_member.save()
	
		context = {
			'project_url': Site.objects.get_current().domain + reverse('cms:edit_project_url', kwargs={'pk': project.pk}),
			'coordinator': project_member.member.user.get_full_name()
		}
		
		subject = 'Project created: %s' % project.title
		message = render_to_string('emails/project_coordinator_email.txt', context)
		send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [project_member.member.user.email])
	
	return members

create_profile.connect(create_profile_handler)
assign_coordinators.connect(assign_coordinators_handler)
