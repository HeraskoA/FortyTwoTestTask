# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserData'
        db.create_table(u'hello_userdata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')(null=True)),
            ('bio', self.gf('django.db.models.fields.TextField')(max_length=256)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=60)),
            ('jabber', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('skype', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('other_contacts', self.gf('django.db.models.fields.TextField')(max_length=256)),
        ))
        db.send_create_signal(u'hello', ['UserData'])


    def backwards(self, orm):
        # Deleting model 'UserData'
        db.delete_table(u'hello_userdata')


    models = {
        u'hello.userdata': {
            'Meta': {'object_name': 'UserData'},
            'bio': ('django.db.models.fields.TextField', [], {'max_length': '256'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '60'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jabber': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'other_contacts': ('django.db.models.fields.TextField', [], {'max_length': '256'}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        }
    }

    complete_apps = ['hello']