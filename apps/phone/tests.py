"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import datetime

from django.conf import settings
from django.test import TestCase

from phone.models import Network


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
