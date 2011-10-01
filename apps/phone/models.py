from django.db import models
from django.contrib.auth.models import User


class Network(models.Model):
    name = models.CharField(max_length=128, unique=True)
    

class Phone(models.Model):
    user = models.ForeignKey(User)
    number = models.CharField(max_length=16, unique=True)
    network = models.ForeignKey(Network)

    def get_short_number(self):
        value = self.number
        if value.startswith('0') or \
            value.startswith('+') or \
            ' ' in value or \
            '-' in value or \
            '.' in value:
            # Remove spaces, dashes and dots
            value = value.replace(' ', '').replace('-', '').replace('.', '')
            # Remove prefix 0 or country code (just Philippines or +63 for now)
            value = value.lstrip('+63').lstrip('0')
        return value

    def save(self, **kw):
        """
        Override default save method
        """
        self.number = self.get_short_number()
        return super(Phone, self).save(**kw)
