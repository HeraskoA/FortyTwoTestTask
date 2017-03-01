# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from hello.models import UserData
from django.core.urlresolvers import reverse
import datetime
from io import BytesIO
from PIL import Image
import json


class TestEdit(TestCase):
    fixtures = ['superuser.json']

    def setUp(self):
        UserData.objects.create(
            first_name="Andrei",
            last_name="Herasko",
            date_of_birth='1998-02-23',
            bio="bio",
            email="andrey.herasko@gmail.com",
            jabber="hector@42cc.co",
            skype="ander2299",
            other_contacts="other",
            photo=self.get_photo()
        )
        self.client = Client()
        self.client.login(username="admin", password="admin")
        self.url = reverse('edit', kwargs={'pk': 1})

    def get_photo(self, width=400, height=400):
        photo = BytesIO()
        image = Image.new("RGB", (width, height), (256, 0, 0))
        image.save(photo, "JPEG")
        photo.name = 'test.jpeg'
        photo.seek(0)
        return photo

    def test_photo_resize(self):
        """ test photo resizing """
        self.client.post(self.url, {
            "first_name": "name",
            "last_name": "lastname",
            "email": "email@mail.ru",
            "jabber": "jabber@42cc.co",
            "date_of_birth": datetime.date(1998, 2, 23),
            "skype": "skype",
            "other_contacts": "other_contacts",
            "bio": "bio",
            "photo": self.get_photo(500, 1000)
        }, follow=True)
        data = UserData.objects.first()
        self.assertEqual(data.photo.width, 100)
        self.assertEqual(data.photo.height, 200)

    def test_form_context(self):
        """check response contex, it should include form and object"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = UserData.objects.first()
        self.assertEqual(response.context['object'], data)
        self.assertTrue(response.context['form'])

    def test_form_displaying(self):
        """data for editing and form and must be presented in the page"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = UserData.objects.first()
        self.assertIn('Name:', response.content)
        self.assertIn('Last name:', response.content)
        self.assertIn('Date of birth:', response.content)
        self.assertIn('Email:', response.content)
        self.assertIn('Jabber:', response.content)
        self.assertIn('name="add_button"', response.content)
        self.assertIn(data.first_name, response.content)
        self.assertIn(data.last_name, response.content)
        self.assertIn(str(data.date_of_birth), response.content)
        self.assertIn(data.email, response.content)
        self.assertIn(data.jabber, response.content)
        self.assertIn(data.photo.url, response.content)

    def test_check_ajax_validation(self):
        """check validation in case ajax"""
        response = self.client.post(
            path=self.url,
            data={
                "first_name": "111",
                "last_name": "111",
                "email": "emailaasfru",
                "jabber": "jabber",
                "date_of_birth": 12312312,
                "skype": "qwer%%",
                "other_contacts": "other_contacts",
                "bio": "bio",
                "photo": self.get_photo()
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        response = json.loads(response.content)
        self.assertEqual(response[u'first_name'], [u'Enter a valid name.'])
        self.assertEqual(response[u'last_name'], [u'Enter a valid name.'])
        self.assertEqual(response[u'email'], [u'Enter a valid email address.'])
        self.assertEqual(response[u'jabber'], [u'Enter a valid jabber.'])
        self.assertEqual(response[u'date_of_birth'], [u'Enter a valid date.'])
        self.assertEqual(response[u'skype'], [u'Enter a valid skype.'])
        data = UserData.objects.first()
        self.assertNotEqual(data.first_name, '111')
        self.assertNotEqual(data.last_name, '111')
        self.assertNotEqual(data.email, 'emailaasfru')
        self.assertNotEqual(data.jabber, 'jabber')
        self.assertNotEqual(data.date_of_birth, 12312312)
        self.assertNotEqual(data.skype, 'qwer%%')

    def test_save_ajax(self):
        """"check save edited data in case ajax request"""
        self.client.post(
            path=self.url,
            data={
                "first_name": "And",
                "last_name": "Rei",
                "email": "asdasd@mail.ru",
                "jabber": "aaa@42cc.co",
                "date_of_birth": datetime.date(1998, 2, 23),
                "skype": "ander1111",
                "other_contacts": "other_contacts",
                "bio": "bio",
                "photo": self.get_photo()
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        data = UserData.objects.first()
        self.assertEqual(data.first_name, 'And')
        self.assertEqual(data.last_name, 'Rei')
        self.assertEqual(data.email, 'asdasd@mail.ru')
        self.assertEqual(data.jabber, 'aaa@42cc.co')
        self.assertEqual(data.date_of_birth, datetime.date(1998, 2, 23))
        self.assertEqual(data.skype, 'ander1111')
        self.assertEqual(data.other_contacts, 'other_contacts')
        self.assertEqual(data.bio, 'bio')
        self.assertTrue(data.photo)

    def test_anon(self):
        """anon user, return 302 status code"""
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_auth(self):
        """authentication user, return status code 200"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_home_view_template(self):
        """check the use of the correct template"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit.html')
