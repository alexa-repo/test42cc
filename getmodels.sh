#!/bin/bash

python manage.py appmodelslist --err-stderr > $(date '+%Y-%m-%d').dat
