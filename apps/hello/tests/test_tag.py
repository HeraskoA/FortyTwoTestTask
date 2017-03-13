# -*- coding: utf-8 -*-
from django.template import Template, Context, TemplateSyntaxError
from django.test import TestCase
from hello.models import UserData


class TestTag(TestCase):
    fixtures = ['data.json']

    def test_tag(self):
        """ test tag with valid object """
        data = UserData.objects.first()
        out = Template(
            "{% load edit_link %}"
            "{% edit_link data %}"
        ).render(Context({"data": data}))
        self.assertIn('/admin/hello/userdata/1', out)

    def test_tag_with_not_valid_obj(self):
        """ test tag with ivalid object """
        with self.assertRaises(TemplateSyntaxError):
            Template("{% load admin_link %}"
                     "{% edit_link data %}").render(
                Context({'data': 'wqwt'})
            )
