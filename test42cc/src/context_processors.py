# -*- coding: utf-8 *-*
from django.conf import settings


def settings_to_context(request):
    """
    Return settings to the context
    :param request:
    :return:
    """
    return dict(SETTINGS=settings)
