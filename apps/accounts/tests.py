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


class AccountsTestCase(TestCase):
    '''
    Base class for the test cases; this sets up a sample user.
    
    '''

    def setUp(self):
        self.sample_user1 = RegistrationProfile.objects.create_inactive_user(**USER_DATA[0])
        self.sample_user1.is_active = True
        self.sample_user1.save()
        self.sample_profile1 = self.sample_user1.userprofile_set.get()
        self.sample_user2 = RegistrationProfile.objects.create_inactive_user(**USER_DATA[1])
        self.sample_profile2 = self.sample_user2.userprofile_set.get()


class AccountsModelTests(AccountsTestCase):
    '''
    Tests for model-oriented funcionality of accounts app.
    '''

    def test_user_profile_created(self):
        '''
        Test that a ``UserProfile`` is created for a new user.
        
        '''
        self.assertEqual(UserProfile.objects.count(), 2)


class AccountsFormTests(AccountsTestCase):
    '''
    Tests for form-oriented funcionality of accounts app.

    '''

    def test_login_form(self):
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
        # test valid data
        form = forms.LoginForm(data={
            'username': USER_DATA[0]['username'],
            'password': USER_DATA[0]['password'],
        })
        self.failUnless(form.is_valid())
        form = forms.LoginForm(data={
            'username': USER_DATA[0]['username'],
            'password': USER_DATA[0]['password'],
            'keep_signed_in': False,
        })
        form.is_valid()
        print form.errors
        self.failUnless(form.is_valid())
        form = forms.LoginForm(data={
            'username': USER_DATA[0]['username'],
            'password': USER_DATA[0]['password'],
            'keep_signed_in': True,
        })
        self.failUnless(form.is_valid())

    def test_user_account_form(self):
        '''
        Tests for account editing.
        We will use the sample_user1
        '''
        invalid_data_dicts = [
            dict(
                data = dict (
                    email = 'bob@example.com',
                ),
                error = (
                    'email',
                    'An account with that email address already exists.',
                ),
            ),
        ]
        for invalid_dict in invalid_data_dicts:
            form = forms.UserAccountForm(instance=self.sample_user1, data=invalid_dict['data'])
            self.failIf(form.is_valid())
            self.assertEqual(form.errors[invalid_dict['error'][0]][0], invalid_dict['error'][1])
        # Change email address
        form = forms.UserAccountForm(instance=self.sample_user1, data={
            'email': 'alice1@example.com',
        })
        self.failUnless(form.is_valid())
        # Change name
        form = forms.UserAccountForm(instance=self.sample_user1, data={
            'first_name': 'Alice',
            'last_name': 'Smith',
        })
        self.failUnless(form.is_valid())


class AccountsViewTests(AccountsTestCase):
    '''
    Tests for the views included in django-registration.

    '''

    def login(self):
        self.client.login(
            username = USER_DATA[0]['username'],
            password = USER_DATA[0]['password'],
        )

    def setUp(self):
        super(AccountsViewTests, self).setUp()
        # Activate sample_user1
        self.sample_user1.is_active = True
        self.sample_user1.save()

    def test_index_view(self):
        response = self.client.get(reverse('accounts-index'))
        self.assertEqual(response.status_code, 200)
        self.failUnless(response.context['in_account_home'])

    def test_postauthcmd_view(self):
        response = self.client.get(reverse('accounts-postauthcmd'))
        self.assertEqual(response.status_code, 200)
        self.failUnless(response.context['post_auth_url'])

    def test_login_view(self):
        # Test showing login form
        response = self.client.get(reverse('accounts-login'))
        self.assertEqual(response.status_code, 200)
        self.failUnless(response.context['form'])
        # Test login post
        response = self.client.post(
            reverse('accounts-login'),
            data = {
                'username': USER_DATA[0]['username'],
                'password': USER_DATA[0]['password'],
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://testserver%s' % reverse('accounts-postauthcmd'))
        # Test invalid login
        response = self.client.post(
            reverse('accounts-login'),
            data = {
                'username': USER_DATA[0]['username'],
                'password': 'invalid',
            }
        )
        self.assertEqual(response.status_code, 200)
        self.failUnless(response.context['form'].errors)

    def test_logout_view(self):
        self.login()
        response = self.client.get(reverse('accounts-logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://testserver%s' % reverse('accounts-postauthcmd'))

    def test_edit_view(self):
        self.login()
        # Get the account edit form
        response = self.client.get(reverse('accounts-edit'))
        self.assertEqual(response.status_code, 200)
        self.failUnless(response.context['form'])
        # Edit account
        response = self.client.post(
            reverse('accounts-edit'),
            data = {
                'email': 'alice1@example.com',
            }
        )
        self.assertEqual(response.status_code, 200)
        self.failUnless(response.context['form'])
        self.failIf(response.context['form'].errors)
        # Edit account using an invalid email
        response = self.client.post(
            reverse('accounts-edit'),
            data = {
                'email': USER_DATA[1]['email'],
            }
        )
        self.assertEqual(response.status_code, 200)
        self.failUnless(response.context['form'])
        self.failUnless(response.context['form'].errors)
        self.assertEqual(response.context['form'].errors['email'][0], 'An account with that email address already exists.')

    def test_details_view(self):
        self.login()
        # Get the account edit form
        response = self.client.get(reverse('accounts-details', args=(self.sample_user1.pk, )))
        self.assertEqual(response.status_code, 200)
        self.failUnless(response.context['user'])
        self.failUnless(response.context['on_user_details_page'])

    def test_user_confirm_email_view(self):
        from django.utils.http import int_to_base36
        from django.contrib.auth.tokens import default_token_generator
        self.login()
        # Test user email confirmation
        response = self.client.get(reverse(
            'accounts-user-confirm-email',
            args=(
                int_to_base36(self.sample_user1.pk),
                default_token_generator.make_token(self.sample_user1)
            )
        ))
        self.assertEqual(response.status_code, 200)
        self.failUnless(response.context['user'])
        self.failUnless(response.context['valid_link'])
