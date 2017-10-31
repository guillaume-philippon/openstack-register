"""
Model to add admin support
"""
from __future__ import unicode_literals

from django.db import models  # pylint: disable=import-error


class UserActivation(models.Model):  # pylint: disable=too-few-public-methods
    """
    UserActivation model
    """
    link = models.TextField(null=False)
    username = models.CharField(max_length=32, null=False)
    expiration_date = models.DateField(auto_now_add=True, auto_now=False)


class UserInfo(models.Model):  # pylint: disable=too-few-public-methods
    """
    make desc.
    """
    username = models.CharField(max_length=32, null=False)
    creation_date = models.DateField(auto_now_add=True, auto_now=False)
    last_agreement = models.DateField(auto_now_add=False, auto_now=False)
    enabled = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    countForce = models.IntegerField(default=0)
    def __unicode__(self):
        return self.username


class GroupInfo(models.Model):  # pylint: disable=too-few-public-methods
    """
    make desc.
    """
    group_name = models.CharField(max_length=32, null=False)
    administrators = models.ManyToManyField(UserInfo, through='IsAdmin')

    def __unicode__(self):
        return self.group_name


class IsAdmin(models.Model):  # pylint: disable=too-few-public-methods
    """
    make desc.
    """
    administrators = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    group = models.ForeignKey(GroupInfo, on_delete=models.CASCADE)
