# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from hello.models import UserData


class TestHomeView(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('home')

    def create_obj(self):
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

    def test_home_view_without_data(self):
        """database is empty, must be presented 'No data' """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('42 Coffee Cups Test Assignment', response.content)
        self.assertIn('No data', response.content)
        self.assertNotIn('Andrei', response.content)
        self.assertNotIn('Herasko', response.content)

    def test_home_view_one_object(self):
        """database coitains 1 object, must be present data in the page"""
        self.create_obj()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('42 Coffee Cups Test Assignment', response.content)
        self.assertIn('Name', response.content)
        self.assertIn('Last name', response.content)
        self.assertIn('Date of birth', response.content)
        self.assertIn('bio', response.content)
        self.assertIn('Email', response.content)
        self.assertIn('Jabber', response.content)
        self.assertIn('Andrei', response.content)
        self.assertIn('Herasko', response.content)
        self.assertIn('Feb. 23, 1998', response.content)
        self.assertIn('andrey.herasko@gmail.com', response.content)
        self.assertIn('hector@42cc.co', response.content)
        self.assertIn('ander2299', response.content)

    def test_home_view_two_object(self):
        """database coitains 2 objects, must be present only the first"""
        self.create_obj()
        UserData.objects.create(
            first_name="aaaaaa",
            last_name="aaaaa",
            date_of_birth='1998-02-23',
            bio="aaa",
            email="aaa@gmail.com",
            jabber="aaaaa",
            skype="aaaaa",
            other_contacts="aaaaa"
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(UserData.objects.first(), response.context['data'])

    def test_home_view_cyrillic(self):
        """Test for views.home in case object data is cyrillic"""
        UserData.objects.create(
            first_name="Андрей",
            last_name="Герасько",
            date_of_birth='1998-02-23',
            bio="Био",
            email="aaa@gmail.com",
            jabber="aaaaa",
            skype="aaaaa",
            other_contacts="Контакты"
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('42 Coffee Cups Test Assignment', response.content)
        self.assertIn('Андрей', response.content)
        self.assertIn('Герасько', response.content)
        self.assertIn('Date of birth', response.content)
        self.assertIn('Био', response.content)
        self.assertIn('Контакты', response.content)

    def test_home_view_template(self):
        """check the use of the correct template"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_data.html')
