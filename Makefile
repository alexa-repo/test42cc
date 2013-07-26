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
    #rm -rf persondb
	PYTHONPATH= $(PYTHONPATH) DJANGO_SETTINGS_MODULE=$(PROJECT).settings $(MANAGE) syncdb --noinput --no-initial-data #--migrate
	PYTHONPATH= $(PYTHONPATH) python manage.py loaddata initial_data.json

clean_db:
	rm -rf persondb
