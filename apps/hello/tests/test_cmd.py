# -*- coding: utf-8 -*-
from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO
from django.db.models import get_models


class TestCmd(TestCase):
    fixtures = ['data.json']

    def test_cmd(self):
        """ test command output"""
        out_stdout = StringIO()
        out_stderr = StringIO()
        call_command('mcount', stdout=out_stdout, stderr=out_stderr)
        for model in get_models():
            out_str = "There are %d objects in %s model" % (
                model.objects.count(),
                model.__name__
            )
            err_str = "error: There are %d objects in %s model" % (
                model.objects.count(),
                model.__name__
            )
        self.assertIn(out_str, out_stdout.getvalue())
        self.assertIn(err_str, out_stderr.getvalue())
