from django.conf import settings
from django.forms import ModelForm, Textarea
from django.utils.safestring import mark_safe
from models import Person
from django import forms
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_unicode
from django.forms.widgets import ClearableFileInput, Input, CheckboxInput


class PersonForm(ModelForm):
    class Meta:
        model = Person
        widgets = {
            'bio': Textarea({'cols' : 40, 'rows' : 10}),
            'other_contacts': Textarea({'cols' : 40, 'rows' : 10}),
            }

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
