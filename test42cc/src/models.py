import datetime
from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    first_name = models.CharField(max_length=60, verbose_name="Name")
    last_name = models.CharField(max_length=60, verbose_name="Surname")
    birth_date = models.DateField(verbose_name="Birthdate")
    bio = models.TextField(verbose_name="Biography")
    email = models.EmailField(max_length=75, verbose_name="E-mail")
    skype = models.CharField(max_length=40, verbose_name="Skype name")
    jabber = models.CharField(max_length=75, verbose_name="Jabber ID")
    other_contacts = models.TextField(verbose_name="Other contacts")
    #image_photo = models.ImageField(verbose_name="Photo", upload_to='images/uploads', null=True, blank=True)

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