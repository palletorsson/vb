# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OrderItem'
        db.create_table(u'orders_orderitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['orders.Order'])),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['products.Article'])),
            ('color', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('color_2', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('pattern', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('pattern_2', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('size', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('quantity', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
        ))
        db.send_create_signal(u'orders', ['OrderItem'])

        # Adding model 'ReaOrderItem'
        db.create_table(u'orders_reaorderitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['orders.Order'])),
            ('reaArticle', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['products.ReaArticle'])),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'orders', ['ReaOrderItem'])


    def backwards(self, orm):
        # Deleting model 'OrderItem'
        db.delete_table(u'orders_orderitem')

        # Deleting model 'ReaOrderItem'
        db.delete_table(u'orders_reaorderitem')


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
        },
        u'orders.orderitem': {
            'Meta': {'ordering': "['date_added']", 'object_name': 'OrderItem'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['products.Article']"}),
            'color': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'color_2': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['orders.Order']"}),
            'pattern': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'pattern_2': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'quantity': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'size': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        u'orders.reaorderitem': {
            'Meta': {'ordering': "['date_added']", 'object_name': 'ReaOrderItem'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['orders.Order']"}),
            'reaArticle': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.ReaArticle']"})
        },
        u'products.article': {
            'Meta': {'object_name': 'Article'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.Category']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'description_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_sv': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'discount': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.Discount']", 'null': 'True', 'blank': 'True'}),
            'file': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'name_sv': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.IntegerField', [], {}),
            'quality': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.Quality']"}),
            'sku_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.Type']"})
        },
        u'products.category': {
            'Meta': {'object_name': 'Category', '_ormbases': [u'products.ChoiceBase']},
            u'choicebase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['products.ChoiceBase']", 'unique': 'True', 'primary_key': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'name_sv': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'})
        },
        u'products.choicebase': {
            'Meta': {'object_name': 'ChoiceBase'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '160'})
        },
        u'products.color': {
            'Meta': {'object_name': 'Color', '_ormbases': [u'products.ChoiceBase']},
            u'choicebase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['products.ChoiceBase']", 'unique': 'True', 'primary_key': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'name_sv': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'quality': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['products.Quality']"})
        },
        u'products.discount': {
            'Meta': {'object_name': 'Discount'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'discount': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'})
        },
        u'products.pattern': {
            'Meta': {'object_name': 'Pattern', '_ormbases': [u'products.ChoiceBase']},
            u'choicebase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['products.ChoiceBase']", 'unique': 'True', 'primary_key': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'name_sv': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'quality': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['products.Quality']"})
        },
        u'products.quality': {
            'Meta': {'object_name': 'Quality', '_ormbases': [u'products.ChoiceBase']},
            u'choicebase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['products.ChoiceBase']", 'unique': 'True', 'primary_key': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'description_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_sv': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'name_sv': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'})
        },
        u'products.reaarticle': {
            'Meta': {'ordering': "['-created']", 'object_name': 'ReaArticle'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.Article']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.Category']"}),
            'color': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.Color']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'json': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'pattern': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.Pattern']"}),
            'quality': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.Quality']"}),
            'rea_price': ('django.db.models.fields.IntegerField', [], {}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['products.Size']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'stockquantity': ('django.db.models.fields.IntegerField', [], {})
        },
        u'products.size': {
            'Meta': {'object_name': 'Size'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'quality': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['products.Quality']"})
        },
        u'products.type': {
            'Meta': {'object_name': 'Type', '_ormbases': [u'products.ChoiceBase']},
            u'choicebase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['products.ChoiceBase']", 'unique': 'True', 'primary_key': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'name_sv': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['orders']