from lettuce import *
from lettuce.django import django_url
from lxml import html
from django.test.client import Client
from django.contrib.auth.models import User


@before.harvest
def prepare_browser(variables):
    #if variables.get('run_server', False):
    world.browser = Client()

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
