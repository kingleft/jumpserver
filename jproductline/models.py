# coding: utf-8

from django.db import models
from django.contrib.auth.models import AbstractUser
import time
# from jasset.models import Asset, AssetGroup

class Department(models.Model):
    name = models.CharField(max_length=32, unique=True, null=False)
    comment = models.CharField(max_length=80)
    def __unicode__(self):
        return '%s' % self.name

class ProductLine(models.Model):
    name = models.CharField(max_length=80, unique=True, null=False)
    department = models.ForeignKey(Department)
    comment = models.CharField(max_length=80)
    def __unicode__(self):
        return '%s: %s' % (self.name, self.department)


