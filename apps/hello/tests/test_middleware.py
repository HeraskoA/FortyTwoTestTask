# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from hello.models import Request
from django.core.urlresolvers import reverse


class TestMiddlware(TestCase):

    def setUp(self):
        self.client = Client()

    def test_get_requests(self):
        """check storing get requests"""
        response = self.client.get(reverse('home'))
        request = Request.objects.first()
        self.assertEqual(response.request['PATH_INFO'], request.path)
        self.assertEqual(response.request['REQUEST_METHOD'], request.method)

    def test_post_requests(self):
        """check storing post requests"""
        response = self.client.post(reverse('requests'))
        request = Request.objects.first()
        self.assertEqual(response.request['PATH_INFO'], request.path)
        self.assertEqual(response.request['REQUEST_METHOD'], request.method)

    def test_count_of_requests(self):
        """check count of saved requests"""
        for i in range(3):
            self.client.get(reverse('home'))
            self.client.post(reverse('home'))
        self.assertEqual(Request.objects.count(), 6)

    def test_ajax_request(self):
        """ajax request, that has 'temp' argument should not be saved"""
        self.client.get(
            path=reverse('requests'),
            data=dict(temp='6'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(Request.objects.count(), 0)
