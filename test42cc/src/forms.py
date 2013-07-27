from django.forms import ModelForm, Textarea
from models import Person
from widget import *


class PersonForm(ModelForm):
    class Meta:
        model = Person
        widgets = dict(bio=Textarea({'cols': 40, 'rows': 10}), other_contacts=Textarea({'cols': 40, 'rows': 10}),
                       image_photo=CustomClearableFileInput(),
                       birth_date=DatePickerWidget(params="dateFormat: 'yy-mm-dd', changeYear: true"))

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
