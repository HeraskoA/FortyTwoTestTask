# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'MyData.photo'
        db.add_column(u'hello_userdata', 'photo',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'MyData.photo'
        db.delete_column(u'hello_userdata', 'photo')


    models = {
        u'hello.userdata': {
            'Meta': {'object_name': 'UserData'},
            'bio': ('django.db.models.fields.TextField', [], {'max_length': '256'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '40'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jabber': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'other_contacts': ('django.db.models.fields.TextField', [], {'max_length': '256'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'hello.request': {
            'Meta': {'object_name': 'Request'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['hello']
