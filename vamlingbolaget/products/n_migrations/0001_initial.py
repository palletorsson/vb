# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Variation'
        db.create_table('products_variation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Article'])),
            ('color', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Color'])),
            ('pattern', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Pattern'])),
        ))
        db.send_create_signal('products', ['Variation'])

        # Adding model 'Image'
        db.create_table('products_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('variation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Variation'])),
            ('is_featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('file', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('products', ['Image'])

        # Adding model 'Size'
        db.create_table('products_size', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('products', ['Size'])

        # Adding model 'Color'
        db.create_table('products_color', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('quality', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Quality'])),
            ('file', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('products', ['Color'])

        # Adding model 'Pattern'
        db.create_table('products_pattern', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('quality', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Quality'])),
            ('file', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('products', ['Pattern'])

        # Adding model 'Quality'
        db.create_table('products_quality', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('products', ['Quality'])

        # Adding model 'Type'
        db.create_table('products_type', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('quality', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Quality'])),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('products', ['Type'])

        # Adding model 'Price'
        db.create_table('products_price', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('price', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('products', ['Price'])

        # Adding model 'Article'
        db.create_table('products_article', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=160)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, blank=True)),
            ('sku_number', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('quality', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Quality'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Type'])),
            ('price', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Price'])),
            ('file', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('products', ['Article'])


    def backwards(self, orm):
        # Deleting model 'Variation'
        db.delete_table('products_variation')

        # Deleting model 'Image'
        db.delete_table('products_image')

        # Deleting model 'Size'
        db.delete_table('products_size')

        # Deleting model 'Color'
        db.delete_table('products_color')

        # Deleting model 'Pattern'
        db.delete_table('products_pattern')

        # Deleting model 'Quality'
        db.delete_table('products_quality')

        # Deleting model 'Type'
        db.delete_table('products_type')

        # Deleting model 'Price'
        db.delete_table('products_price')

        # Deleting model 'Article'
        db.delete_table('products_article')


    models = {
        'products.article': {
            'Meta': {'object_name': 'Article'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'price': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Price']"}),
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
        'products.image': {
            'Meta': {'object_name': 'Image'},
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'variation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Variation']"})
        },
        'products.pattern': {
            'Meta': {'object_name': 'Pattern'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'quality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Quality']"})
        },
        'products.price': {
            'Meta': {'object_name': 'Price'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.IntegerField', [], {})
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
        },
        'products.variation': {
            'Meta': {'object_name': 'Variation'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Article']"}),
            'color': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Color']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'pattern': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Pattern']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['products']