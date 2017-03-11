# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from chat.models import Dialog, Message
from datetime import time
import json


class TestDialogView(TestCase):

    fixtures = ['data.json']

    def setUp(self):
        self.client = Client()
        self.client.login(username="admin", password="admin")
        self.url = reverse('dialog', kwargs={'pk': 2})
        self.count = Message.objects.count()

    def create_messages(self):
        self.client.get(self.url)
        sender1 = User.objects.first()
        sender2 = User.objects.last()
        dialog = Dialog.objects.first()
        for i in range(10):
            Message.objects.create(
                text='text',
                sender=sender1,
                dialog=dialog
                )
        for i in range(10):
            Message.objects.create(
                text='text',
                sender=sender2,
                dialog=dialog
                )

    def test_displaing_data(self):
        """check displaing data"""
        self.create_messages()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        for message in Message.objects.all():
            self.assertIn(
                message.text.encode('ascii', 'ignore'),
                response.content)
            self.assertIn(
                message.sender.username.encode('ascii', 'ignore'),
                response.content
                )
        self.assertEqual(len(response.context['messages']), 20)

    def test_save_message(self):
        """check saving message"""
        self.client.post(
            path=self.url,
            data={
                "message": "ajax"
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        new_count = Message.objects.count()
        last_message = Message.objects.last().text
        self.assertEqual(new_count, self.count+1)
        self.assertEqual(last_message, 'ajax')

    def test_get_messages_ajax(self):
        """test get last unread messages"""
        self.create_messages()
        response = self.client.get(
            path=self.url,
            data={
                "count": 5
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        messages = Message.objects.all()[5:]
        required_response = []
        for message in messages:
            required_response.append({
                'text': message.text,
                'sender': message.sender.username,
                'time': time.strftime(message.date, "%H:%M")
            })
        required_response = json.dumps(required_response)
        self.assertEqual(response.content, required_response)

    def test_save_empty_message(self):
        """empty message should not be saved """
        self.client.post(
            path=self.url,
            data={
                "message": " "
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        new_count = Message.objects.count()
        self.assertEqual(new_count, self.count)

    def test_stripped(self):
        """
        all spaces should be stripped from
        the beginning and the end of the message
        """
        self.client.post(
            path=self.url,
            data={
                "message": "   sas asf     "
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        last_message = Message.objects.last().text
        self.assertEqual(last_message, "sas asf")

    def test_cyrillic_message(self):
        """check saving cyrillic message"""
        self.client.post(
            path=self.url,
            data={
                "message": "сообщение"
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        new_count = Message.objects.count()
        last_message = Message.objects.last().text
        self.assertEqual(new_count, self.count+1)
        self.assertEqual(last_message, u'сообщение')

    def test_dialog_view_template(self):
        """check the use of the correct template"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dialog.html')
