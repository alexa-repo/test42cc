from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    birth_date = models.DateField()
    bio = models.TextField()
    email = models.EmailField(max_length=75)
    skype = models.CharField(max_length=40)
    jabber = models.CharField(max_length=75)
    contacts = models.TextField()

    def _get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    full_name = property(_get_full_name)

    def __unicode__(self):
        return u"%s %s" % (self.last_name, self.first_name)