# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Checkout'
        db.create_table('checkout_checkout', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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
            ('post', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('checkout', ['Checkout'])


    def backwards(self, orm):
        # Deleting model 'Checkout'
        db.delete_table('checkout_checkout')


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
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'post': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        }
    }

    complete_apps = ['checkout']