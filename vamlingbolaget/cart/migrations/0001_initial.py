# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Cart'
        db.create_table('cart_cart', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('cart', ['Cart'])

        # Adding model 'CartItem'
        db.create_table('cart_cartitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cart', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['cart.Cart'])),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['products.Article'])),
            ('color', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('color_2', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('pattern', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('pattern_2', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('size', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('quantity', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
        ))
        db.send_create_signal('cart', ['CartItem'])


    def backwards(self, orm):
        # Deleting model 'Cart'
        db.delete_table('cart_cart')

        # Deleting model 'CartItem'
        db.delete_table('cart_cartitem')


    models = {
        'cart.cart': {
            'Meta': {'object_name': 'Cart'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'cart.cartitem': {
            'Meta': {'ordering': "['date_added']", 'object_name': 'CartItem'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['products.Article']"}),
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['cart.Cart']"}),
            'color': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'color_2': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pattern': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'pattern_2': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'size': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'products.article': {
            'Meta': {'object_name': 'Article'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Category']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'description_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_sv': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'discount': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Discount']", 'null': 'True', 'blank': 'True'}),
            'file': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'name_sv': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.IntegerField', [], {}),
            'quality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Quality']"}),
            'sku_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Type']"})
        },
        'products.category': {
            'Meta': {'object_name': 'Category', '_ormbases': ['products.ChoiceBase']},
            'choicebase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['products.ChoiceBase']", 'unique': 'True', 'primary_key': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'name_sv': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'})
        },
        'products.choicebase': {
            'Meta': {'object_name': 'ChoiceBase'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '160'})
        },
        'products.discount': {
            'Meta': {'object_name': 'Discount'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'discount': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'})
        },
        'products.quality': {
            'Meta': {'object_name': 'Quality', '_ormbases': ['products.ChoiceBase']},
            'choicebase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['products.ChoiceBase']", 'unique': 'True', 'primary_key': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'description_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_sv': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'name_sv': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'})
        },
        'products.type': {
            'Meta': {'object_name': 'Type', '_ormbases': ['products.ChoiceBase']},
            'choicebase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['products.ChoiceBase']", 'unique': 'True', 'primary_key': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'name_sv': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['cart']