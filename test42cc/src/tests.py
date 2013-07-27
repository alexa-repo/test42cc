from django.core.urlresolvers import reverse
from django.http.request import HttpRequest
from django.template import RequestContext
from django.test import TestCase
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

    def test_request(self):
        response = self.client.get('admin/auth/user/1/')
        req = HttpStoredQuery.objects.latest('id')
        self.assertEqual('admin/auth/user/1/', req.path)


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


