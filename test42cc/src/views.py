# -*- coding: utf-8 -*-
from django.core.serializers import json
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from models import Person, HttpStoredQuery
from django.shortcuts import render
from test42cc.src.forms import PersonForm


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


def edit_person_entry(request):
    """
    View for edit current Person entry
    :param itemId:
    :param request:
    :return:
    """
    entry = None
    try:
        entry = Person.objects.get(pk=1)
    except Person.DoesNotExist:
        pass

    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES, instance=entry)
        if form.is_valid():
            if request.FILES:
                form.cleaned_data['image_photo'] = request.FILES['image_photo']
            form.save()
            return HttpResponse(json.dumps(dict(status=0, redirect=reverse('edit'))))
    else:
        form = PersonForm(instance=entry)
        return render(request, 'edit.html', locals())