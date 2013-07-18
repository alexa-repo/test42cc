from django.test import TestCase
from models import Person

class PersonTestCase(TestCase):
    """
    Test for model Person and main page
    """
    fixtures = ['data.json']

    def setUp(self):
        pass

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        person = Person.objects.get(pk=1)
        self.assertEqual(str(person.first_name), 'Alexandra')
        self.assertEqual(str(person.last_name), 'Mihailjuk')
        self.assertEqual(str(person.birth_date.strftime("%Y-%m-%d")), '1987-11-19')
        self.assertEqual(str(person.bio), 'this is my bio')
        self.assertEqual(str(person.email), 'alexa.sandra.mail@gmail.com')
        self.assertEqual(str(person.jabber), 'alexa_sandra@jabber.ru')
        self.assertEqual(str(person.skype), 'alexa_sandra_')