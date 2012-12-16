# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Checkout.order'
        db.add_column('checkout_checkout', 'order',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Checkout.order'
        db.delete_column('checkout_checkout', 'order')


    models = {
        'checkout.checkout': {
            'Meta': {'object_name': 'Checkout'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'order': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'post': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        }
    }

    complete_apps = ['checkout']