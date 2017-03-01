# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from hello.models import UserData, Request
from django.db.models import (CharField,
                              DateField, TimeField,
                              TextField, EmailField)


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
        self.assertEqual(type(first_name), CharField)
        self.assertEqual(type(last_name), CharField)
        self.assertEqual(type(date_of_birth), DateField)
        self.assertEqual(type(bio), TextField)
        self.assertEqual(type(email), EmailField)
        self.assertEqual(type(jabber), CharField)
        self.assertEqual(type(skype), CharField)
        self.assertEqual(type(other_contacts), TextField)


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
