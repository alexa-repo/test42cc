SHELL := /bin/bash

MANAGE=django-admin.py
PROJECT=test42cc

clean:
	-rm *~*
	-find . -name '*.pyc' -exec rm {} \;

runserver:
	PYTHONPATH=$(PYTHONPATH) python manage.py runserver

test:
	#python manage.py test src


syncdb:clean_db
    PYTHONPATH= `pwd`/test42cc DJANGO_SETTINGS_MODULE=$(PROJECT).settings $(MANAGE) syncdb --noinput --no-initial-data #--migrate
	PYTHONPATH= `pwd`/test42cc python manage.py loaddata data.json

clean_db:
	rm -rf persondb
