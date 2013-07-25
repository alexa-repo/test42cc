from django.core.urlresolvers import reverse
from django.http.request import HttpRequest
from django.template import RequestContext
from django.test import TestCase
from models import Person, HttpStoredQuery
from test42cc.src.forms import PersonForm


class PersonTestCase(TestCase):
    """
    Test for model Person and main page
    """
    fixtures = ['initial_data.json']

    def setUp(self):
        pass

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        person = Person.objects.get(pk=1)
        self.assertEqual(str(person.first_name), 'Alexandra')
        self.assertEqual(str(person.last_name), 'Mihailjuk')
        self.assertEqual(str(person.birth_date.strftime("%Y-%m-%d")), '1987-11-19')
        self.assertEqual(str(person.bio), '<br /><br />this is my bio')
        self.assertEqual(str(person.email), 'alexa.sandra.mail@gmail.com')
        self.assertEqual(str(person.jabber), 'alexa_sandra@jabber.ru')
        self.assertEqual(str(person.skype), 'alexa_sandra_')


class HttpQueriesMiddlewareTest(TestCase):
    """
    Test middleware
    """

    def setUp(self):
        pass

    def test_request(self):
        response = self.client.get('admin/auth/user/1/')
        req = HttpStoredQuery.objects.latest('id')
        self.assertEqual('admin/auth/user/1/', req.path)


class ContextProcessorTest(TestCase):
    """
    Test contextProcessor
    """

    def test_settings_in_context(self):
        try:
            default_context = RequestContext(HttpRequest())
            self.assertTrue(default_context.has_key('SETTINGS'))
        except ImportError:
            pass


class EditPersonEntryTest(TestCase):
    """
    Test edit form
    """
    def setUp(self):
        pass

    def test_edit_account(self):
        pass
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        entry = Person.objects.get(pk=1)
        form = PersonForm(instance=entry)
        #print reverse("edit", )
        response = self.client.get(reverse("edit"), data=form)
        self.assertEqual(response.status_code, 200)

        entry['birth_date'] = '1987-12-28'

        self.client.post(reverse("edit"), data=entry)
        self.failUnlessEqual(response.status_code, 302)"""

