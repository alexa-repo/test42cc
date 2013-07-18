SHELL := /bin/bash

MANAGE=django-admin.py
PROJECT=test42cc

clean:
	-rm *~*
	-find . -name '*.pyc' -exec rm {} \;

runserver:
	PYTHONPATH=$(PYTHONPATH) python manage.py runserver

test:
	PYTHONPATH=$(PYTHONPATH) DJANGO_SETTINGS_MODULE=$(PROJECT).settings $(MANAGE) test src


syncdb: clean_db
	PYTHONPATH= $(PYTHONPATH) DJANGO_SETTINGS_MODULE=$(PROJECT).settings $(MANAGE) syncdb --noinput --no-initial-data #--migrate
	PYTHONPATH= $(PYTHONPATH) python manage.py loaddata data.json

clean_db:
	rm -rf persondb
	#-find path -type f -name "persondb" -delete
