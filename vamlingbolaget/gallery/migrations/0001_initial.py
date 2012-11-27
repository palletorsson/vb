# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Gallery'
        db.create_table('gallery_gallery', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('feature_image', self.gf('filebrowser.fields.FileBrowseField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('gallery', ['Gallery'])

        # Adding model 'Image'
        db.create_table('gallery_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='default', max_length=50)),
            ('image', self.gf('filebrowser.fields.FileBrowseField')(max_length=200, null=True, blank=True)),
            ('variation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Variation'], null=True, blank=True)),
            ('is_featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('gallery', ['Image'])

        # Adding M2M table for field gallery on 'Image'
        db.create_table('gallery_image_gallery', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('image', models.ForeignKey(orm['gallery.image'], null=False)),
            ('gallery', models.ForeignKey(orm['gallery.gallery'], null=False))
        ))
        db.create_unique('gallery_image_gallery', ['image_id', 'gallery_id'])


    def backwards(self, orm):
        # Deleting model 'Gallery'
        db.delete_table('gallery_gallery')

        # Deleting model 'Image'
        db.delete_table('gallery_image')

        # Removing M2M table for field gallery on 'Image'
        db.delete_table('gallery_image_gallery')


    models = {
        'gallery.gallery': {
            'Meta': {'object_name': 'Gallery'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'feature_image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'gallery.image': {
            'Meta': {'object_name': 'Image'},
            'gallery': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['gallery.Gallery']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '50'}),
            'variation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Variation']", 'null': 'True', 'blank': 'True'})
        },
        'products.article': {
            'Meta': {'object_name': 'Article'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'file': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'price': ('django.db.models.fields.IntegerField', [], {}),
            'quality': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Quality']"}),
            'sku_number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Type']"})
        },
        'products.choicebase': {
            'Meta': {'object_name': 'ChoiceBase'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '160'})
        },
        'products.color': {
            'Meta': {'object_name': 'Color', '_ormbases': ['products.ChoiceBase']},
            'choicebase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['products.ChoiceBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        'products.pattern': {
            'Meta': {'object_name': 'Pattern', '_ormbases': ['products.ChoiceBase']},
            'choicebase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['products.ChoiceBase']", 'unique': 'True', 'primary_key': 'True'})
        },
        'products.quality': {
            'Meta': {'object_name': 'Quality', '_ormbases': ['products.ChoiceBase']},
            'choicebase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['products.ChoiceBase']", 'unique': 'True', 'primary_key': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {})
        },
        'products.type': {
            'Meta': {'object_name': 'Type', '_ormbases': ['products.ChoiceBase']},
            'choicebase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['products.ChoiceBase']", 'unique': 'True', 'primary_key': 'True'})
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

    complete_apps = ['gallery']