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


