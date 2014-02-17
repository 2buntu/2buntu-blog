# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Ad'
        db.create_table(u'ads_ad', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('display_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('display_end', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'ads', ['Ad'])


    def backwards(self, orm):
        # Deleting model 'Ad'
        db.delete_table(u'ads_ad')


    models = {
        u'ads.ad': {
            'Meta': {'object_name': 'Ad'},
            'display_end': ('django.db.models.fields.DateTimeField', [], {}),
            'display_start': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'product': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['ads']