from django.contrib.auth.models import User
from django.http import HttpResponse

from utils import json

def check_email(request):
    status = 422
    message = _(u'Invalid email address.')
    content = dict()
    if 'POST' == request.method:
        if request.POST.get('email'):
            email = request.POST.get('email').strip()
            if len(email):
                try:
                    user = User.objects.get(email=email)
                    message = _(u'Email address is already registered. Please use another email address.')
                except User.DoesNotExist:
                    status = 200
                    message = _(u'Email address is available.')
    return HttpResponse(
        json.get_json(
            request,
            status,
            message,
            content
        )
    )

def check_username(request):
    status = 422
    message = _(u'Invalid username.')
    content = dict()
    if 'POST' == request.method:
        if request.POST.get('username'):
            username = request.POST.get('username').strip()
            if len(username):
                try:
                    user = User.objects.get(username=username)
                    message = _(u'Username is NOT available.')
                except User.DoesNotExist:
                    status = 200
                    message = _(u'Username is available.')
    return HttpResponse(
        json.get_json(
            request,
            status,
            message,
            content
        )
    )
