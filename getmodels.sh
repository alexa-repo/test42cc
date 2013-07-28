#!/bin/bash

python manage.py appmodelslist person --err-stderr > $(date '+%Y-%m-%d').dat
