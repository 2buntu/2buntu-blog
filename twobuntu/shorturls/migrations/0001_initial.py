# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ShortURL'
        db.create_table(u'shorturls_shorturl', (
            ('key', self.gf('django.db.models.fields.CharField')(default='92364b', max_length=6, primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'shorturls', ['ShortURL'])


    def backwards(self, orm):
        # Deleting model 'ShortURL'
        db.delete_table(u'shorturls_shorturl')


    models = {
        u'shorturls.shorturl': {
            'Meta': {'object_name': 'ShortURL'},
            'key': ('django.db.models.fields.CharField', [], {'default': "'29f2cf'", 'max_length': '6', 'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['shorturls']