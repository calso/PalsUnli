"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import datetime

from django.conf import settings
from django.test import TestCase

from registration.models import RegistrationProfile
from phone.models import Network, Phone


class NetworkTestCase(TestCase):
    """
    Base class for Network related test cases.
    """

    def setUp(self):
        """
        Setup necessary properties for Network tests
        """
        # Create default Smart and Globe network that would be a property
        # of the other test case classes
        self.smart = Network.objects.create(name='Smart')
        self.globe = Network.objects.create(name='Globe')


class NetworkModelTestCase(NetworkTestCase):
    """
    Tests for model-oriented functionality
    """

    def test_create_network(self):
        """
        Test creating a new network
        """
        # Remove smart and globe because we'll add this as a default property
        #smart = Network.objects.create(name='Smart')
        #globe = Network.objects.create(name='Globe')
        sun = Network.objects.create(name='Sun')
        red = Network.objects.create(name='Red')

    def test_read_network(self):
        """
        Test reading network details.
        """
        # Test getting network with pk=1
        assert(Network.objects.get(pk=1))
        # Test getting network with name=Globe
        assert(Network.objects.get(name='Globe'))

    def test_update_network(self):
        """
        Test updating of existing networks
        """
        self.smart.name = 'Smart Philippines'
        self.smart.save()
        self.globe.name = 'Globe Philippines'
        self.globe.save()

    def test_delete_network(self):
        """
        Test deleting existing networks
        """
        self.smart.delete()
        self.globe.delete()


class PhoneTestCase(TestCase):
    """
    Base class for Phone related test cases
    """

    def setUp(self):
        """
        Setup necessary properties for Phone tests
        """
        self.smart = Network.objects.create(name='Smart')
        self.globe = Network.objects.create(name='Globe')
        # Create a user for our tests
        self.user1 = RegistrationProfile.objects.create_inactive_user(
            username='alice',
            password='secret',
            email='alice@example.com',
        )
        self.user1.is_active = True
        self.user1.save()

        self.user2 = RegistrationProfile.objects.create_inactive_user(
            username='bobby',
            password='12345',
            email='bobby@example.com',
        )
        self.user2.is_active = True
        self.user2.save()


class PhoneModelTestCase(PhoneTestCase):
    """
    Tests for model-oriented functionality of the Phone model
    """

    def test_create_phone(self):
        """
        Test creating new phone
        """
        phone1 = Phone.objects.create(
            user = self.user1,
            network = self.smart,
            number = '+63 918 765 4321'
        )

        phone2 = Phone.objects.create(
            user = self.user2,
            network = self.globe,
            number = '+63 915 765 4020'
        )
