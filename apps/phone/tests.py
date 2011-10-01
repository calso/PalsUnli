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
    Base class for Network model related test cases.
    """

    def setUp(self):
        """
        Setup necessary properties for Network tests
        """
        self.smart = Network.objects.create(name='Smart')


class NetworkModelTestCase(NetworkTestCase):
    """
    Tests for model-oriented functionality
    """

    def test_create_network(self):
        """
        Test creating a new network
        """
        smart = Network.objects.create(name='Smart')
        globe = Network.objects.create(name='Globe')
        sun = Network.objects.create(name='Sun')
        red = Network.objects.create(name='Red')


