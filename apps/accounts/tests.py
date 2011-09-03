'''
Unit tests for palsunli accounts app.

These tests assume that you've completed all the prerequisites for
getting django-registration running in the default setup, to wit:

1. You have ``accounts`` in your ``INSTALLED_APPS`` setting.

2. You have created all of the templates mentioned in this
   application's documentation.

3. You have added all the settings mentioned in the application's
   documentation.

4. You have URL patterns pointing to all the views for the accounts
   application

'''

import datetime
import sha

from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.core import management
from django.core.urlresolvers import reverse
from django.test import TestCase

from registration.models import RegistrationProfile
from accounts.models import UserProfile
from accounts import forms

USER_DATA = dict(
    username='alice',
    password='secret',
    email='alice@example.com',
)


class AccountsTestCase(TestCase):
    '''
    Base class for the test cases; this sets up a sample user.
    
    '''

    def setUp(self):
        self.sample_user = RegistrationProfile.objects.create_inactive_user(**USER_DATA)
        self.sample_profile = self.sample_user.userprofile_set.get()


class AccountsModelTests(AccountsTestCase):
    '''
    Tests for model-oriented funcionality of accounts app.
    '''

    def test_user_profile_created(self):
        '''
        Test that a ``UserProfile`` is created for a new user.
        
        '''
        self.assertEqual(UserProfile.objects.count(), 1)


class AccountsFormTests(AccountsTestCase):
    '''
    Tests for form-oriented funcionality of accounts app.

    '''

    def test_login(self):
        '''
        Tests for logins

        '''
        error = (
            '__all__',
            'Please enter a correct username and password. Note that both fields are case-sensitive.',
        )
        invalid_data_dicts = [
            dict(
                data = dict(
                    username = 'alice',
                    password = 'invalid',
                ),
                error = error,
            ),
            dict(
                data = dict(
                    username = 'invalid',
                    password = 'secret',
                ),
                error = error,
            ),
            dict(
                data = dict(
                    username = 'invalid',
                    password = 'invalid',
                ),
                error = error,
            ),
        ]
        for invalid_dict in invalid_data_dicts:
            form = forms.LoginForm(data=invalid_dict['data'])
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[invalid_dict['error'][0]][0], invalid_dict['error'][1])
        form = forms.LoginForm(data={
            'username': USER_DATA['username'],
            'password': USER_DATA['password'],
        })
        form = forms.LoginForm(data={
            'username': USER_DATA['username'],
            'password': USER_DATA['password'],
            'keep_signed_in': False,
        })
        form = forms.LoginForm(data={
            'username': USER_DATA['username'],
            'password': USER_DATA['password'],
            'keep_signed_in': True,
        })
