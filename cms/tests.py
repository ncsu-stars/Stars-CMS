from django.test import SimpleTestCase
from cms.models import *
import cms
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

class ProjectTest(SimpleTestCase):
    def setUp(self):
        self.tearDown()
        Project.objects.create(title="Project1", status=Project.STATUS_ACTIVE, year=cms.academic_year(cms.get_current_time()))

    def test_get_absolute_url(self):
        project = Project.objects.get(pk=1)
        expectedUrl = "/project/all/2014/#1"
        self.assertEqual(project.get_absolute_url(), expectedUrl)

    def test_is_member_coordinator_no_members(self):
        Member.objects.create(status=Member.STATUS_ACTIVE, user=User.objects.create())
        project = Project.objects.get(pk=1)
        member = Member.objects.get(pk=1)
        self.assertFalse(project.is_member_coordinator(member))

    def test_is_member_coordinator_member_is_coordinator(self):
        Member.objects.create(status=Member.STATUS_ACTIVE, user=User.objects.create())
        project = Project.objects.get(pk=1)
        member = Member.objects.get(pk=1)
        ProjectMember.objects.create(project=project, member=member, is_coordinator=True)
        self.assertTrue(project.is_member_coordinator(member))

    def test_is_member_coordinator_member_is_not_coordinator(self):
        Member.objects.create(status=Member.STATUS_ACTIVE, user=User.objects.create())
        project = Project.objects.get(pk=1)
        member = Member.objects.get(pk=1)
        ProjectMember.objects.create(project=project, member=member, is_coordinator=False)
        self.assertFalse(project.is_member_coordinator(member))

    def test_get_status(self):
        Project.objects.create(title="Project2", status=Project.STATUS_ARCHIVED, year=cms.academic_year(cms.get_current_time()))
        Project.objects.create(title="Project3", status=Project.STATUS_EMPTY, year=cms.academic_year(cms.get_current_time()))
        self.assertEqual(3, len(Project.objects.all()))
        project1 = Project.objects.get(title="Project1")
        project2 = Project.objects.get(title="Project2")
        project3 = Project.objects.get(title="Project3")

        self.assertEqual(u"Active", project1.get_status_display())
        self.assertEqual(u"Archived", project2.get_status_display())
        self.assertEqual(u"Empty", project3.get_status_display())

    def test_get_category(self):
        Project.objects.create(status=Project.STATUS_ARCHIVED, category=Project.CATEGORY_INTERNSHIP, year=cms.academic_year(cms.get_current_time()))
        Project.objects.create(status=Project.STATUS_EMPTY, category=Project.CATEGORY_ORGANIZATIONAL, year=cms.academic_year(cms.get_current_time()))
        Project.objects.create(status=Project.STATUS_ARCHIVED, category=Project.CATEGORY_OUTREACH, year=cms.academic_year(cms.get_current_time()))
        Project.objects.create(status=Project.STATUS_EMPTY, category=Project.CATEGORY_SERVICE, year=cms.academic_year(cms.get_current_time()))
        Project.objects.create(status=Project.STATUS_ARCHIVED, category=Project.CATEGORY_RESEARCH, year=cms.academic_year(cms.get_current_time()))

        project1 = Project.objects.get(pk=1)
        project2 = Project.objects.get(pk=2)
        project3 = Project.objects.get(pk=3)
        project4 = Project.objects.get(pk=4)
        project5 = Project.objects.get(pk=5)
        project6 = Project.objects.get(pk=6)

        self.assertEqual("Other", project1.get_category_display())
        self.assertEqual("Internship", project2.get_category_display())
        self.assertEqual("Organizational", project3.get_category_display())
        self.assertEqual("Outreach", project4.get_category_display())
        self.assertEqual("Service", project5.get_category_display())
        self.assertEqual("Research", project6.get_category_display())

    def tearDown(self):
        Member.objects.all().delete()
        User.objects.all().delete()
        Project.objects.all().delete()

class ProjectMemberTest(SimpleTestCase):
    def setUp(self):
        self.tearDown()
        Member.objects.create(user=User.objects.create(username="1", first_name="First", last_name="Last"), status=Member.STATUS_ACTIVE)
        Project.objects.create(title="Project2", status=Project.STATUS_ARCHIVED, year=cms.academic_year(cms.get_current_time()))
        ProjectMember.objects.create(project=Project.objects.get(pk=1), member=Member.objects.get(pk=1))
        ProjectMember.objects.create(project=Project.objects.get(pk=1), volunteer_name="Volunteer")

    def test_get_full_name_from_volunteer(self):
        self.assertEqual(u"Volunteer", ProjectMember.objects.get(pk=2).get_full_name())

    def test_get_full_name_from_member(self):
        project_member = ProjectMember.objects.get(pk=1)
        self.assertFalse(project_member.is_volunteer())
        self.assertEqual(User.objects.get(pk=1).get_full_name(), project_member.get_full_name())

    def test_is_volunteer(self):
        self.assertFalse(ProjectMember.objects.get(pk=1).is_volunteer())
        self.assertTrue(ProjectMember.objects.get(pk=2).is_volunteer())

    def test__unicode__non_role(self):
        project_member = ProjectMember.objects.get(pk=1)

        self.assertEquals("First Last", unicode(project_member))

    def test__unicode__role(self):
        ProjectMember.objects.create(project=Project.objects.get(pk=1), member=Member.objects.get(pk=1),
                                     role="Cool Kids")
        role_project = ProjectMember.objects.get(pk=3)
        self.assertEquals("First Last (Cool Kids)", unicode(role_project))


    def tearDown(self):
        User.objects.all().delete()
        Project.objects.all().delete()
        Member.objects.all().delete()

class NewsTest(SimpleTestCase):
    news = None
    def setUp(self):
        News.objects.create(title="News1!", description="THis is a description.", content="Just some content",
                            date=cms.get_current_time())
        self.news = News.objects.get(pk=1)

    def test__unicode__(self):
        self.assertEqual("News1!", unicode(self.news))
