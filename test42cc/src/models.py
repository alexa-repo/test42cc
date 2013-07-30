import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete


class Person(models.Model):
    first_name = models.CharField(max_length=60, verbose_name="Name")
    last_name = models.CharField(max_length=60, verbose_name="Surname")
    birth_date = models.DateField(verbose_name="Birthdate")
    bio = models.TextField(verbose_name="Biography")
    email = models.EmailField(max_length=75, verbose_name="E-mail")
    skype = models.CharField(max_length=40, verbose_name="Skype name")
    jabber = models.CharField(max_length=75, verbose_name="Jabber ID")
    other_contacts = models.TextField(verbose_name="Other contacts")
    image_photo = models.ImageField(verbose_name="Photo",
                                    upload_to='images/uploads', null=True,
                                    blank=True)

    def _get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    full_name = property(_get_full_name)

    def __unicode__(self):
        return u"%s %s" % (self.last_name, self.first_name)


class HttpStoredQuery(models.Model):
    path = models.CharField(max_length=300)
    method = models.CharField(max_length=20)
    user = models.ForeignKey(User, blank=True, null=True)
    date_with_time = models.DateTimeField(auto_now_add=True,
                                          default=datetime.datetime.now())
    priority = models.IntegerField(default=1)


class ModelsActions(models.Model):
    """
    Model for store changes in models app
    """
    CREATE_ACTION = 0
    UPDATE_ACTION = 1
    DELETE_ACTION = 2

    STATUS_CHOICES = (
        (CREATE_ACTION, 'create'),
        (UPDATE_ACTION, 'update'),
        (DELETE_ACTION, 'delete'),
    )

    action = models.IntegerField(choices=STATUS_CHOICES, default=CREATE_ACTION)
    model_name = models.CharField(max_length=75)
    change_obj_id = models.PositiveIntegerField()
    date_with_time = models.DateTimeField(auto_now=True)


def save_model_signal(sender, **kwargs):
    """
    Save data by post save signal. Ignore model ModelsActions
    """
    instance = kwargs['instance']
    if sender == ModelsActions or type(instance.pk) != int:
        return

    mod = ModelsActions()
    mod.model_name = sender.__name__
    mod.change_obj_id = instance.pk
    if not kwargs['created']:
        mod.action = ModelsActions.UPDATE_ACTION
    mod.save()


def delete_model_signal(sender, **kwargs):
    """
    Save entry about delete some object from model. Ignore model ModelsActions
    """
    instance = kwargs['instance']
    if sender == ModelsActions or type(instance.pk) != int:
        return

    mod = ModelsActions()
    mod.model_name = sender.__name__
    mod.change_obj_id = instance.pk
    mod.action = ModelsActions.DELETE_ACTION
    mod.save()


post_save.connect(save_model_signal)
post_delete.connect(delete_model_signal)