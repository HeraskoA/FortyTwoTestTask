from django.db import models


class UserData(models.Model):
    first_name = models.CharField(max_length=256, blank=False)
    last_name = models.CharField(max_length=256, blank=False)
    date_of_birth = models.DateField(blank=False, null=True)
    bio = models.TextField(max_length=256, blank=False)
    email = models.EmailField(max_length=60, blank=False)
    jabber = models.CharField(max_length=40, blank=False)
    skype = models.CharField(max_length=40, blank=False)
    other_contacts = models.TextField(max_length=256, blank=False)


class Request(models.Model):
    path = models.CharField(max_length=60, blank=True)
    method = models.CharField(max_length=60, blank=True)
    time = models.TimeField(blank=True, auto_now=True)
