# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class TestChatView(TestCase):

    fixtures = ['data.json']

    def setUp(self):
        self.client = Client()
        self.url = reverse('chat')
        self.client.login(username="admin", password="admin")

    def test_displaing_data(self):
        """check displaing data on the page"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Chat', response.content)
        self.assertIn('select the user', response.content)
        self.assertIn('Users', response.content)
        for user in User.objects.all():
            self.assertIn(user.username, response.content)

    def test_home_view_template(self):
        """check the use of the correct template"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chat.html')
