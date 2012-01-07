from django.core.management.base import BaseCommand
from django.conf import settings

import os

from cms.models import Member, Project, MEMBER_IMAGE_FOLDER, PROJECT_IMAGE_FOLDER

class Command(BaseCommand):
    args = ''
    help = 'Removes unused files and folders from media/'

    def handle(self, *args, **kwargs):
        member_active_files = [ os.path.join(settings.MEDIA_ROOT, x) for x in Member.objects.all().values_list('image', flat=True) ]
        member_base = os.path.join(settings.MEDIA_ROOT, MEMBER_IMAGE_FOLDER)

        project_active_files = [ os.path.join(settings.MEDIA_ROOT, x) for x in Project.objects.all().values_list('image', flat=True) ]
        project_base = os.path.join(settings.MEDIA_ROOT, PROJECT_IMAGE_FOLDER)

        for (base, active_files) in [ (member_base, member_active_files), (project_base, project_active_files) ]:
            for root, dirs, files in os.walk(base):
                for f in files:
                    path = os.path.join(root, f)
                    if not path in active_files:
                        os.unlink(path)
                        print 'removed unused file %s' % (path,)

