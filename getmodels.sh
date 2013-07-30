#!/bin/bash

python manage.py appmodelslist 2> $(date '+%Y-%m-%d').dat
