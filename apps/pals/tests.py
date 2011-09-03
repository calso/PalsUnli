"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase

from registration.models import RegistrationProfile

USER_DATA = [
    dict(
        username='alice',
        password='secret',
        email='alice@example.com',
    ),
    dict(
        username='bob',
        password='secret',
        email='bob@example.com',
    ),
]


class PalsTestCase(TestCase):
    '''
    Base class for the test cases; this sets up 2 sample user.
    '''

    def setUp(self):
        self.sample_user1 = RegistrationProfile.objects.create_inactive_user(**USER_DATA[0])
        self.sample_user2 = RegistrationProfile.objects.create_inactive_user(**USER_DATA[1])
        self.sample_user1.is_active = True
        self.sample_user2.is_active = True
        self.sample_user1.save()
        self.sample_user2.save()


class PalsModelTestCase(PalsTestCase):
    '''
    Tests for model-specific functionality
    '''


class PalsFormTestCase(PalsTestCase):
    '''
    Tests for form-specific functionality
    '''


class PalsViewTestCase(PalsTestCase):
    '''
    Tests for view-specific functionality
    '''
