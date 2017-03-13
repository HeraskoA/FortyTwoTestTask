# -*- coding: utf-8 -*-
from django.test import TestCase
from hello.models import UserData, Request, ActionHistory
from django.db.models import (CharField, ImageField,
                              DateField, TimeField,
                              TextField, EmailField,
                              IntegerField)


class Testdata(TestCase):
    def setUp(self):
        UserData.objects.create(
            first_name="Andrei",
            last_name="Herasko",
            date_of_birth='1998-02-23',
            bio="bio",
            email="andrey.herasko@gmail.com",
            jabber="hector@42cc.co",
            skype="ander2299",
            other_contacts="other"
        )

    def test_model(self):
        """Check models field"""
        data = UserData.objects.first()
        first_name = data._meta.get_field('first_name')
        last_name = data._meta.get_field('last_name')
        date_of_birth = data._meta.get_field('date_of_birth')
        bio = data._meta.get_field('bio')
        email = data._meta.get_field('email')
        jabber = data._meta.get_field('jabber')
        skype = data._meta.get_field('skype')
        other_contacts = data._meta.get_field('other_contacts')
        photo = data._meta.get_field('photo')
        self.assertEqual(type(first_name), CharField)
        self.assertEqual(type(last_name), CharField)
        self.assertEqual(type(date_of_birth), DateField)
        self.assertEqual(type(bio), TextField)
        self.assertEqual(type(email), EmailField)
        self.assertEqual(type(jabber), CharField)
        self.assertEqual(type(skype), CharField)
        self.assertEqual(type(other_contacts), TextField)
        self.assertEqual(type(photo), ImageField)


class TestRequestModel(TestCase):
    def setUp(self):
        Request.objects.create(
            path="/",
            method="GET",
        )

    def test_model(self):
        """Check models field"""
        req = Request.objects.first()
        path = req._meta.get_field('path')
        method = req._meta.get_field('method')
        time = req._meta.get_field('time')
        self.assertEqual(type(method), CharField)
        self.assertEqual(type(path), CharField)
        self.assertEqual(type(time), TimeField)


class TestActionHistoryModel(TestCase):
    def test_model(self):
        """Check models fields"""
        ActionHistory.objects.create(
            object_type='User',
            object_id=1,
            action='create'
        )
        instance = ActionHistory.objects.first()
        object_type = instance._meta.get_field('object_type')
        object_id = instance._meta.get_field('object_id')
        action = instance._meta.get_field('action')
        self.assertEqual(type(object_type), CharField)
        self.assertEqual(type(object_id), IntegerField)
        self.assertEqual(type(action), CharField)
