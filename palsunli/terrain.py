from lettuce import *
from lettuce.django import django_url
from lxml import html

from django.test.utils import setup_test_environment, teardown_test_environment
from django.core.management import call_command
from django.db import connection
from django.conf import settings

from django.test.client import Client
from django.contrib.auth.models import User

# Reference: http://cilliano.com/blog/2011/02/07/django-bdd-with-lettuce-and-splinter/

@before.harvest
def initial_setup(server):
    call_command('syncdb', interactive=False, verbosity=0)
    call_command('flush', interactive=False, verbosity=0)
    call_command('migrate', interactive=False, verbosity=0)
    call_command('loaddata', 'all', verbosity=0)
    setup_test_environment()
    #if variables.get('run_server', False):
    world.browser = Client()

@after.harvest
def cleanup(server):
    connection.creation.destroy_test_db(settings.DATABASES['default']['NAME'])
    teardown_test_environment()

@step(u'I access the url "([^"]*)"')
def access_url(step, url):
    full_url = django_url(url)
    response = world.browser.get(full_url)
    world.dom = html.fromstring(response.content)

@step(u'a user "([^"]*)" with password "([^"]*)"')
def create_user(step, username, password):
    user, new = User.objects.get_or_create(username=username, email='%s@example.com' % username)
    user.set_password(password)
    user.save()

@step(u'login as "([^"]*)" with password "([^"]*)"')
def login(step, username, password):
    #user = User.objects.get(username=username, password=password)
    world.browser.post('/accounts/login', {'username': username, 'password': password})
    world.browser.login(username = username, password = password)
