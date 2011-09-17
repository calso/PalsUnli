from django.db import models
from django.contrib.auth.models import User


class Network(models.Model):
    name = models.CharField(max_length=128, unique=True)
    

class Phone(models.Model):
    user = models.ForeignKey(User)
    number = models.CharField(max_length=16, unique=True)
    network = models.ForeignKey(Network)
