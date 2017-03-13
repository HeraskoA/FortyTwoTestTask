# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.auth.models import User
from chat.models import Dialog, Message
from django.db.models import CharField, ForeignKey


class TestMessage(TestCase):

    fixtures = ['data.json']

    def test_model(self):
        """Check models field"""
        user1 = User.objects.first()
        user2 = User.objects.last()
        dialog = Dialog.objects.create(user1=user1, user2=user2)
        Message.objects.create(
            text="text",
            dialog=dialog,
            sender=user1
            )
        message = Message.objects.first()
        text = message._meta.get_field('text')
        sender = message._meta.get_field('sender')
        dialog = message._meta.get_field('dialog')
        self.assertEqual(type(text), CharField)
        self.assertEqual(type(sender), ForeignKey)
        self.assertEqual(type(dialog), ForeignKey)


class TestDialog(TestCase):

    fixtures = ['data.json']

    def test_model(self):
        """Check models field"""
        user1 = User.objects.first()
        user2 = User.objects.last()
        dialog = Dialog.objects.create(user1=user1, user2=user2)
        dialog = Dialog.objects.first()
        user1 = dialog._meta.get_field('user1')
        user2 = dialog._meta.get_field('user2')
        self.assertEqual(type(user1), ForeignKey)
        self.assertEqual(type(user2), ForeignKey)
