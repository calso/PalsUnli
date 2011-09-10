from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.http import base36_to_int
from django.utils.translation import ugettext, ugettext_lazy as _

import datetime

def index(request):
    '''
    This view is used as the 'dashboard' for user phone functions.

    * URL Name

      ``phone-index``

    * Available Context

      ``in_phone_home`` - Always set to ``True`` when we are in this view.

    * Template

      'phone/index.html'

    '''
    context = dict(in_phone_home=True)

    return render_to_response(
        'phone/index.html',
        context,
        context_instance=RequestContext(request)
    )

