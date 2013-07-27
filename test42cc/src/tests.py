from django.core.urlresolvers import reverse
from django.http.request import HttpRequest
from django.template import RequestContext
from django.test import TestCase
from django.contrib.auth.models import User
from models import Person, HttpStoredQuery


class PersonTestCase(TestCase):
    """
    Test for model Person and main page
    """
    fixtures = ['initial_data.json']

    def test_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        person = Person.objects.get(pk=1)
        #check data in selection entry
        self.assertEqual(str(person.first_name), 'Alexandra')
        self.assertEqual(str(person.last_name), 'Mihailjuk')
        self.assertEqual(str(person.birth_date.strftime("%Y-%m-%d")), '1987-11-19')
        self.assertEqual(str(person.bio), '<br /><br />this is my bio')
        self.assertEqual(str(person.email), 'alexa.sandra.mail@gmail.com')
        self.assertEqual(str(person.jabber), 'alexa_sandra@jabber.ru')
        self.assertEqual(str(person.skype), 'alexa_sandra_')
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
        url = reverse('admin:%s_%s_change' % (user_object._meta.app_label, user_object._meta.module_name),
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
        self.assertTrue(default_context.has_key('SETTINGS'))


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
        self.assertContains(response, '<form method="POST" action="../" enctype="multipart/form-data" id="form_id">')
        self.assertContains(response, '<input id="id_first_name" maxlength="60" '
                                      'name="first_name" type="text" value="%s" />' % entry["first_name"])

    def test_edit_account(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        entry = Person.objects.values().get(pk=1)
        self.assertTrue(self.client.login(username='admin', password='admin'))
        self.client.post(reverse('edit'), data=entry)
        entry['birth_date'] = '1987-12-28'
        self.client.post(reverse("edit"), data=entry)
        self.failUnlessEqual(response.status_code, 200)


