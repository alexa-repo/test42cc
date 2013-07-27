from django.forms import ModelForm, Textarea
from django.utils.safestring import mark_safe
from models import Person
from django.forms.widgets import ClearableFileInput, Input


class CustomClearableFileInput(ClearableFileInput):
    def render(self, name, value, attrs=None):
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': '',
        }
        template = '%(input)s'
        substitutions['input'] = Input.render(self, name, value, attrs)

        return mark_safe(template % substitutions)


class PersonForm(ModelForm):
    class Meta:
        model = Person
        widgets = {
            'bio': Textarea({'cols': 40, 'rows': 10}),
            'other_contacts': Textarea({'cols': 40, 'rows': 10}),
            'image_photo': CustomClearableFileInput(),
        }

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
