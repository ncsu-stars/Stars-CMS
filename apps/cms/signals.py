from django.dispatch import Signal

from models import Member

create_profile = Signal(providing_args=['user', 'group', 'classification'])

def create_profile_handler(sender, **kwargs):
    user = kwargs.get('user', None)
    group = kwargs.get('group', None)
    classification = kwargs.get('classification', None)
    
    profile = Member(user=user, group=group, status=0, classification=classification)
    profile.save()
    
create_profile.connect(create_profile_handler)