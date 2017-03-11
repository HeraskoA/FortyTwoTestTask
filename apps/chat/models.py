# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Dialog(models.Model):
    user1 = models.ForeignKey(User, related_name='+')
    user2 = models.ForeignKey(User, related_name='+')


class Message(models.Model):
    text = models.CharField(max_length=256)
    sender = models.ForeignKey(User)
    dialog = models.ForeignKey(Dialog)
    date = models.TimeField(auto_now_add=True)
