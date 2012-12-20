# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Checkout.order_number'
        db.add_column('checkout_checkout', 'order_number',
                      self.gf('django.db.models.fields.IntegerField')(default=1, blank=True),
                      keep_default=False)

        # Adding field 'Checkout.status'
        db.add_column('checkout_checkout', 'status',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=1, blank=True),
                      keep_default=False)

        # Adding field 'Checkout.session_key'
        db.add_column('checkout_checkout', 'session_key',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Checkout.order_number'
        db.delete_column('checkout_checkout', 'order_number')

        # Deleting field 'Checkout.status'
        db.delete_column('checkout_checkout', 'status')

        # Deleting field 'Checkout.session_key'
        db.delete_column('checkout_checkout', 'session_key')


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
            'order_number': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'post': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'session_key': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        }
    }

    complete_apps = ['checkout']