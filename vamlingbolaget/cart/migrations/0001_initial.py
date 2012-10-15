# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CartItem'
        db.create_table('cart_cartitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cart_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Article'])),
            ('color', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Color'])),
            ('pattern', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Pattern'])),
            ('size', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Size'])),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('quantity', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
        ))
        db.send_create_signal('cart', ['CartItem'])


    def backwards(self, orm):
        # Deleting model 'CartItem'
        db.delete_table('cart_cartitem')


    models = {
        'cart.cartitem': {
            'Meta': {'ordering': "['date_added']", 'object_name': 'CartItem'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Article']"}),
            'cart_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'color': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Color']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pattern': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Pattern']"}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Size']"})
        },
        'products.article': {
            'Meta': {'object_name': 'Article'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'price': ('django.db.models.fields.IntegerField', [], {}),
            'quality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Quality']"}),
            'sku_number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Type']"})
        },
        'products.color': {
            'Meta': {'object_name': 'Color'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'quality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Quality']"})
        },
        'products.pattern': {
            'Meta': {'object_name': 'Pattern'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'quality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Quality']"})
        },
        'products.quality': {
            'Meta': {'object_name': 'Quality'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'products.size': {
            'Meta': {'object_name': 'Size'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'products.type': {
            'Meta': {'object_name': 'Type'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'quality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Quality']"})
        }
    }

    complete_apps = ['cart']