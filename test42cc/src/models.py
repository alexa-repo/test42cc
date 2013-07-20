import datetime
from django.db import models
from django.contrib.auth.models import User

class Person(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    birth_date = models.DateField()
    bio = models.TextField()
    email = models.EmailField(max_length=75)
    skype = models.CharField(max_length=40)
    jabber = models.CharField(max_length=75)
    other_contacts = models.TextField()

    def _get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    full_name = property(_get_full_name)

    def __unicode__(self):
        return u"%s %s" % (self.last_name, self.first_name)


class HttpStoredQuery(models.Model):
    path = models.CharField(max_length=300)
    method = models.CharField(max_length=20)
    user = models.ForeignKey(User, blank=True, null=True)
    date_with_time = models.DateTimeField(auto_now=True, default=datetime.datetime.now())