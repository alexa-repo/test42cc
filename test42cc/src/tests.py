import datetime
import sys
from StringIO import StringIO
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.http.request import HttpRequest
from django.template import RequestContext, Template, Context
from django.test import TestCase
from django.contrib.auth.models import User
from models import Person, HttpStoredQuery, ModelsActions
from forms import PersonForm
from widget import DatePickerWidget


class PersonTestCase(TestCase):
    """
    Test for model Person and main page
    """
    fixtures = ['initial_data.json']

    def test_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        person = Person.objects.get(pk=1)
        #check that data is on the main page
        self.assertContains(response, person.first_name)
        self.assertContains(response, person.last_name)
        self.assertContains(response, person.birth_date.strftime("%Y-%m-%d"))
        self.assertContains(response, person.email)
        self.assertContains(response, person.jabber)
        self.assertContains(response, person.skype)


class HttpQueriesMiddlewareTest(TestCase):
    """
    Test middleware
    """

    def test_add_request(self):
        user_object = User.objects.get(pk=1)
        url = reverse('admin:%s_%s_change' % (user_object._meta.app_label,
                                              user_object._meta.module_name),
                      args=[user_object.id])
        response = self.client.get(url)
        req = HttpStoredQuery.objects.latest('id')
        self.assertEqual(response._request.path, req.path)

    def test_requests_count(self):
        #generate requests
        COUNT_SHOW_REQ = 10
        urls = ['/%d' % n for n in range(COUNT_SHOW_REQ + 2)]
        for url in urls:
            self.client.get(url)

        response = self.client.get(reverse('requests'))
        self.assertContains(response, '<h4>HTTP Requests</h4>')
        self.assertContains(response, '<td>%s</td>' % urls[0])

        for url in urls[:COUNT_SHOW_REQ]:
            self.assertContains(response, '<td>%s</td>' % url)

        for url in urls[COUNT_SHOW_REQ:]:
            self.assertNotContains(response, '<td>%s</td>' % url)


class ContextProcessorTest(TestCase):
    """
    Test contextProcessor
    """

    def test_settings_in_context(self):
        default_context = RequestContext(HttpRequest())
        self.assertTrue('SETTINGS' in default_context)
        self.failUnlessEqual(default_context['SETTINGS'].SECRET_KEY,
                             "vj7medpba*4ht*y4e&54)cxqooqu)v=0_d6ku3910hc6^bh6nx")
        self.failUnlessEqual(default_context['SETTINGS'].ROOT_URLCONF,
                             "test42cc.urls")


class EditPersonEntryTest(TestCase):
    """
    Test edit form
    """

    def test_auth_for_form(self):
        entry = Person.objects.values().get(pk=1)
        url = reverse('edit')

        # Authorization
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        # Logging in
        self.assertTrue(self.client.login(username='admin', password='admin'))
        response = self.client.get(url)
        self.assertContains(response, '<form method="POST" action="" enctype="multipart/form-data" id="form_id">')
        self.assertContains(response, '<input id="id_first_name" maxlength="60" '
                                      'name="first_name" type="text" value="%s" />' % entry["first_name"])

    def test_edit_account(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        entry = Person.objects.values().get(pk=1)
        self.assertTrue(self.client.login(username='admin', password='admin'))
        self.client.post(reverse('edit'), data=entry)
        entry['birth_date'] = '1987-12-28'
        self.client.post(reverse("edit"), data=entry)
        self.failUnlessEqual(response.status_code, 200)
        new_entry = Person.objects.values().get(pk=1)
        self.assertEquals(entry['birth_date'],
                          new_entry['birth_date'].strftime("%Y-%m-%d"))

    def test_edit_form_contains_widget(self):
        entry = Person.objects.get(pk=1)
        form = PersonForm(instance=entry)
        widgets_list = []
        for field in form:
            widgets_list.append(field.field.widget.__class__.__name__)
        self.assertTrue(DatePickerWidget.__name__ in widgets_list)

    def test_ajax_save_edit_form(self):
        response = self.client.get(reverse('edit'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='admin', password='admin')

        # Valid user
        response = self.client.get(reverse('edit'))
        self.assertEqual(response.status_code, 200)

        entry = Person.objects.values().get(pk=1)
        entry['birth_date'] = '1987-12-28'
        self.client.post(reverse("edit"), data=entry,
                         HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = self.client.get(reverse('edit'))
        self.assertTrue('<!DOCTYPE HTML>' in response.content)

        for k in entry.keys():
            self.assertContains(response, k)
            self.assertContains(response, unicode(entry[k]))

        #Error in form
        entry['birth_date'] = ''
        response = self.client.post(reverse("edit"), data=entry,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertContains(response, 'This field is required')


class EditLinkTagTest(TestCase):
    """
    Test for template tag for edit object from template in admin site
    """

    def setUp(self):
        self.obj = Person.objects.get(pk=1)

    def testEditLinkObject(self):
        link = reverse('admin:%s_%s_change' % (self.obj._meta.app_label,
                                               self.obj._meta.module_name),
                       args=[self.obj.id])
        t = Template('{% load edit_link %}{% admin_link obj %}')
        self.client.login(username="admin", password="admin")
        c = Context({"obj": self.obj})
        result = t.render(c)
        self.assertEqual(link, result)


class TestSignals(TestCase):
    def test_signals(self):
        """
        user = Person(2, "New Name", "LastName",
                      datetime.datetime.strptime("30 Nov 00", "%d %b %y").date(),
                      "bio", "mail@mail.com", "name_", "my_jabber@djabber.com",
                      "other")
        user.save()

        record = ModelsActions.objects.latest('date_with_time')
        self.assertEqual(record.action, 0)

        user.bio = "This is new Biography"
        user.save()
        record = ModelsActions.objects.latest('date_with_time')
        self.assertEqual(record.action, 1)

        user.delete()
        record = ModelsActions.objects.latest('date_with_time')

        self.assertEqual(record.action, 2)
        """


class ModelsListCommandTest(TestCase):
    def test_command(self):
        from django.db.models import get_models
        """
        output = sys.stdout = StringIO()
        call_command('appmodelslist', 'src')
        sys.stdout = sys.__stdout__
        for model in get_models('src'):
            self.assertEqual(output.getvalue().find(model.__name__), 0)

        outputerr = sys.stderr = StringIO()
        call_command('appmodelslist', 'src', prefix='--err-stderr')
        sys.stderr = sys.__stderr__
        for model in get_models('src'):
            self.assertTrue(outputerr.getvalue().find('err'))
            self.assertEqual(outputerr.getvalue().\
                        find('error:%s' % model.__name__))
        """