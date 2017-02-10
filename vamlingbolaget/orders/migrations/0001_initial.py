# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Order'
        db.create_table(u'orders_order', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('postcode', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('message', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('ip', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('shippingAdress', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('order_log', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('payment_key', self.gf('django.db.models.fields.CharField')(max_length=34, blank=True)),
            ('post', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('paymentmethod', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('order_number', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('session_key', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
        ))
        db.send_create_signal(u'orders', ['Order'])


    def backwards(self, orm):
        # Deleting model 'Order'
        db.delete_table(u'orders_order')


    models = {
        u'orders.order': {
            'Meta': {'object_name': 'Order'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'order_log': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'order_number': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'payment_key': ('django.db.models.fields.CharField', [], {'max_length': '34', 'blank': 'True'}),
            'paymentmethod': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'post': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'session_key': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'shippingAdress': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        }
    }

    complete_apps = ['orders']