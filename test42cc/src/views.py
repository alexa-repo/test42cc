# -*- coding: utf-8 -*-
from models import Person, HttpStoredQuery
from django.shortcuts import render


def index(request):
    """
    View for main page: render page with personal data
    :param request:
    :return:
    """
    try:
        contact = Person.objects.get(pk=1)
    except Person.DoesNotExist:
        contact = None
    return render(request, 'index.html', {'contact': contact})


def stored_requests(request):
    try:
        req = HttpStoredQuery.objects.all().order_by('-date_with_time')[:10]
    except HttpStoredQuery.DoesNotExist:
        req = []
    return render(request, 'requests.html', dict(request_list=req))