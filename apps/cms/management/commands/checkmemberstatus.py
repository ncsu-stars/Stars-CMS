from django.core.management.base import BaseCommand
from django.core.management import CommandError
from django.conf import settings
from django.db.models import Q

from django.contrib.auth.models import User
from cms.models import Member

from sys import stdin
import re

ncsu_email_regex = re.compile(r'(?P<unity_id>[a-zA-Z0-9._%+-]+)@ncsu\.edu')
name_regex = re.compile(r'^[-a-zA-z]+$')


class Command(BaseCommand):
    args = '<file>'
    help = 'Checks that all members listed in <file> are active/empty and that all others are inactive'

    def handle(self, *args, **kwargs):
        if len(args) == 0:
            raise CommandError('Missing <file> argument')

        if args[0] == '-':
            f = stdin
        else:
            try:
                f = open(args[0], 'r')
            except IOError as e:
                raise CommandError('Unable to open file "%s": %s' % (args[0], e.message))

        listed_members = []

        for l in f.readlines():
            l = l.strip()

            # try to extract a Unity id
            match = re.search(ncsu_email_regex, l)
            if match:
                user_id = match.groupdict()['unity_id']
                # retrieve User using Unity id
                try:
                    user = User.objects.get(username=user_id)
                    # found
                    listed_members += [ user.get_profile() ]
                    print 'found %s by user id %s' % (user.get_full_name(), user_id)
                    # and done
                    continue
                except User.DoesNotExist:
                    # not found, try another method
                    pass

            # try to extract a name
            names = filter(lambda x: re.match(name_regex, x), l.split(' '))
            # require at least first and last name
            if len(names) >= 2:
                # search by last name
                try:
                    user = User.objects.get(last_name=names[-1])
                    # found with unique last name
                    listed_members += [ user.get_profile() ]
                    print 'found %s by unique last name %s' % (user.get_full_name(), names[-1])
                    # and done
                    continue
                except User.MultipleObjectsReturned:
                    # check first name
                    candidates = filter(lambda x: names[0] in x.first_name, User.objects.filter(last_name=names[-1]))
                    if len(candidates) == 1:
                        # found with unique first and last name pair
                        user = candidates[0]
                        listed_members += [ user.get_profile() ]
                        print 'found %s by unique first and last name pair %s %s' % (user.get_full_name(), names[0], names[-1])
                        # and done
                        continue
                    else:
                        # not found, try another method
                        pass
                except User.DoesNotExist:
                    # not found, try another method
                    pass

            # give up and ask operator
            user = None
            while user is None:
                user_id = raw_input('Which username belongs with %s?: ' % (l, ))
                try:
                    user = User.objects.get(username=user_id)
                    # found with operator assistance
                    listed_members += [ user.get_profile() ]
                    print 'found %s with operator assistance' % (user.get_full_name(),)
                    # and done
                    break
                except User.DoesNotExist:
                    print 'username %s not found' % (user_id,)

        listed_pks = map(lambda x: x.pk, listed_members)

        members_to_activate = Member.objects.filter(pk__in=listed_pks, status=Member.STATUS_ARCHIVED)
        members_to_archive = Member.objects.filter(~Q(pk__in=listed_pks) & ~Q(status=Member.STATUS_ARCHIVED))

        print '====== ACTIVATE ======'
        for m in members_to_activate:
            print m.user.get_full_name()

        print '====== ARCHIVE ======='
        for m in members_to_archive:
            print m.user.get_full_name()

        if len(members_to_activate) == 0 and len(members_to_archive) == 0:
            print 'Nothing to do'
            raise SystemExit

        if raw_input('Does this look right? [y/N] ').lower() != 'y':
            print 'Aborted'
            raise SystemExit

        for m in members_to_activate:
            m.status = Member.STATUS_ACTIVE
            m.save()

            m.user.active = True
            m.user.save()

        for m in members_to_archive:
            m.status = Member.STATUS_ARCHIVED
            m.save()

            m.user.active = False
            m.user.save()

        print 'Done'



