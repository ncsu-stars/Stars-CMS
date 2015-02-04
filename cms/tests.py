from django.test import SimpleTestCase
from cms.models import User
from cms.models import Member
from cms.models import Project
from cms.models import ProjectMember
from django.conf import settings
import django.db.models.query
import hashlib
from django.db import IntegrityError

class MemberTest(SimpleTestCase):
    def setUp(self):
        pass
        User.objects.all().delete() # Have to delete all users because Django doesn't handle that
        Member.objects.create(user=User.objects.create(username="user1", first_name="Random", last_name="User"), group="Undergraduate", classification="freshman",
                              status=Member.STATUS_ACTIVE)

    def test__unicode__(self):
        member_as_unicode = Member.objects.get(pk=1).__unicode__()

        self.assertIsInstance(member_as_unicode, unicode)
        self.assertEqual(unicode("Random User"), member_as_unicode)

    def test_get_coordinated_projects(self):
        member1 = Member.objects.get(pk=1)
        Project.objects.create(title="Project1", description="Blah", status=1, category=0,
                               year=settings.CURRENT_YEAR)
        expectedProject = Project.objects.get(title="Project1")
        ProjectMember.objects.create(project=expectedProject, member=member1, role="Coordinator", is_coordinator=True)

        actualProjects = member1.get_coordinated_projects()
        self.assertIsInstance(actualProjects, django.db.models.query.QuerySet)
        self.assertEqual(1, len(actualProjects))
        actualProject = actualProjects.iterator().next()
        self.assertIsInstance(actualProject, Project)
        self.assertEqual(actualProject, expectedProject)

    def test_get_absolute_url(self):
        member1 = Member.objects.get(pk=1)
        expectedUrl = "/people/1/"
        self.assertEqual(member1.get_absolute_url(), expectedUrl)

    def test_generate_hashed_email_with_empty_email(self):
        member1 = Member.objects.get(pk=1)
        expectedEmail = hashlib.md5("").hexdigest()
        self.assertEqual(expectedEmail, member1.generate_hashed_email())

    def test_generate_hashed_email_email(self):
        user = User.objects.get(pk=1)
        user.email = "test@email.com"
        user.save()

        member1 = Member.objects.get(pk=1)
        expectedEmail = hashlib.md5("test@email.com").hexdigest()
        self.assertEqual(expectedEmail, member1.generate_hashed_email())

    def test_get_possible_project_members(self):
        Member.objects.create(user=User.objects.create(username="user2"), group="Undergraduate", classification="freshman",
                              status=Member.STATUS_ARCHIVED)
        validProjectMember = Member.objects.get(pk=1)
        invalidProjectMember = Member.objects.get(pk=2)

        actualProjectMembers = Member.get_possible_project_members()

        self.assertIsInstance(actualProjectMembers, django.db.models.query.QuerySet)
        self.assertEqual(1, len(actualProjectMembers))
        actualProjectMember = actualProjectMembers.iterator().next()
        self.assertIsInstance(actualProjectMember, Member)
        self.assertEqual(validProjectMember, actualProjectMember)
        self.assertNotEqual(invalidProjectMember, actualProjectMember)

    def test_get_possible_project_members_no_project_members(self):
        projectMember = Member.objects.get(pk=1)
        projectMember.status = Member.STATUS_ARCHIVED
        projectMember.save()

        actualProjectMembers = Member.get_possible_project_members()

        self.assertIsInstance(actualProjectMembers, django.db.models.query.QuerySet)
        self.assertEqual(0, len(actualProjectMembers))

    def test_correct_status(self):
        Member.objects.create(user=User.objects.create(username="user2", first_name="Random", last_name="User"), group="Undergraduate", classification="freshman",
                              status=Member.STATUS_ARCHIVED)
        Member.objects.create(user=User.objects.create(username="user3", first_name="Random", last_name="User"), group="Undergraduate", classification="freshman",
                              status=Member.STATUS_EMPTY)

        member1 = Member.objects.get(pk=1)
        member2 = Member.objects.get(pk=2)
        member3 = Member.objects.get(pk=3)

        self.assertEqual(u"Active", member1.get_status_display())
        self.assertEqual(u"Archived", member2.get_status_display())
        self.assertEqual(u"Empty", member3.get_status_display())

    def test_member_creation(self):
        Member.objects.create(user=User.objects.create(username="user2"), classification="freshman",
                              hometown="hometown", interests="", homepage="", blurb="", status=Member.STATUS_ARCHIVED)
        Member.objects.create(user=User.objects.create(username="user3"), group="Undergraduate", hometown="hometown",
                              interests="", homepage="", blurb="", status=Member.STATUS_ARCHIVED)
        Member.objects.create(user=User.objects.create(username="user4"), group="Undergraduate",
                              classification="freshman", interests="", homepage="", blurb="",
                              status=Member.STATUS_ARCHIVED)
        Member.objects.create(user=User.objects.create(username="user5"), group="Undergraduate", hometown="hometown",
                              classification="freshman", homepage="", blurb="", status=Member.STATUS_ARCHIVED)
        Member.objects.create(user=User.objects.create(username="user6"), group="Undergraduate", hometown="hometown",
                              interests="", classification="freshman", blurb="", status=Member.STATUS_ARCHIVED)
        Member.objects.create(user=User.objects.create(username="user7"), group="Undergraduate", hometown="hometown",
                              interests="", homepage="", classification="freshman", status=Member.STATUS_ARCHIVED)
        with self.assertRaisesRegexp(IntegrityError, "NOT NULL.*cms_member.status"):
            Member.objects.create(user=User.objects.create(username="user8"), group="Undergraduate", hometown="hometown",
                              interests="", homepage="", blurb="", classification="freshman")
        with self.assertRaisesRegexp(IntegrityError, "NOT NULL.*cms_member.user_id"):
            Member.objects.create(group="Undergraduate", classification="freshman", hometown="hometown", interests="",
                              homepage="", blurb="", status=Member.STATUS_ARCHIVED)
        with self.assertRaisesRegexp(IntegrityError, "UNIQUE.*auth_user.username"):
            Member.objects.create(user=User.objects.create(username="user7"), group="Undergraduate", hometown="hometown",
                              interests="", homepage="", classification="freshman", status=Member.STATUS_ARCHIVED)
