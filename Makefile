SHELL := /bin/bash

MANAGE=django-admin.py
PROJECT=test42cc

clean:
	-rm *~*
	-find . -name '*.pyc' -exec rm {} \;

runserver:
	PYTHONPATH=$(PYTHONPATH) python manage.py runserver

test:
	python manage.py test src


syncdb:
    PYTHONPATH= $(PYTHONPATH) DJANGO_SETTINGS_MODULE=$(PROJECT).settings $(MANAGE) syncdb --noinput --migrate

