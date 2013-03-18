# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GalleryStatus'
        db.create_table('gallery_gallerystatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('name_sv', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('display_on_gallery_page', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('display_on_index_page', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('order', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('gallery', ['GalleryStatus'])

        # Adding model 'Gallery'
        db.create_table('gallery_gallery', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('name_sv', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gallery.GalleryStatus'])),
            ('feature_image', self.gf('filebrowser.fields.FileBrowseField')(max_length=200, null=True, blank=True)),
            ('flatpage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['flatpages.FlatPage'], null=True, blank=True)),
        ))
        db.send_create_signal('gallery', ['Gallery'])

        # Adding model 'Photographer'
        db.create_table('gallery_photographer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('gallery', ['Photographer'])

        # Adding model 'Image'
        db.create_table('gallery_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default=' ', max_length=255)),
            ('name_sv', self.gf('django.db.models.fields.CharField')(default=' ', max_length=255, null=True, blank=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(default=' ', max_length=255, null=True, blank=True)),
            ('image', self.gf('filebrowser.fields.FileBrowseField')(max_length=200, null=True, blank=True)),
            ('photographer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gallery.Photographer'], null=True, blank=True)),
            ('gallery', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gallery.Gallery'], null=True, blank=True)),
            ('variation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.Variation'], null=True, blank=True)),
            ('is_featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('order', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('gallery', ['Image'])


    def backwards(self, orm):
        # Deleting model 'GalleryStatus'
        db.delete_table('gallery_gallerystatus')

        # Deleting model 'Gallery'
        db.delete_table('gallery_gallery')

        # Deleting model 'Photographer'
        db.delete_table('gallery_photographer')

        # Deleting model 'Image'
        db.delete_table('gallery_image')


    models = {
        'flatpages.flatpage': {
            'Meta': {'ordering': "('url',)", 'object_name': 'FlatPage', 'db_table': "'django_flatpage'"},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'content_sv': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'enable_comments': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'registration_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title_sv': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        'gallery.gallery': {
            'Meta': {'object_name': 'Gallery'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'feature_image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'flatpage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['flatpages.FlatPage']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'name_sv': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gallery.GalleryStatus']"})
        },
        'gallery.gallerystatus': {
            'Meta': {'object_name': 'GalleryStatus'},
            'display_on_gallery_page': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'display_on_index_page': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'name_sv': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'gallery.image': {
            'Meta': {'object_name': 'Image'},
            'gallery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gallery.Gallery']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "' '", 'max_length': '255'}),
            'name_en': ('django.db.models.fields.CharField', [], {'default': "' '", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_sv': ('django.db.models.fields.CharField', [], {'default': "' '", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'photographer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gallery.Photographer']", 'null': 'True', 'blank': 'True'}),
            'variation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Variation']", 'null': 'True', 'blank': 'True'})
        },
        'gallery.photographer': {
            'Meta': {'object_name': 'Photographer'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
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
        'products.color': {
            'Meta': {'object_name': 'Color', '_ormbases': ['products.ChoiceBase']},
            'choicebase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['products.ChoiceBase']", 'unique': 'True', 'primary_key': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'name_sv': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'quality': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['products.Quality']"})
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
        'products.pattern': {
            'Meta': {'object_name': 'Pattern', '_ormbases': ['products.ChoiceBase']},
            'choicebase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['products.ChoiceBase']", 'unique': 'True', 'primary_key': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'name_sv': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'quality': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['products.Quality']"})
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
        },
        'products.variation': {
            'Meta': {'object_name': 'Variation'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Article']"}),
            'color': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Color']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'pattern': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['products.Pattern']"})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['gallery']