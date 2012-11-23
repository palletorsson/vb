# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'MyProfile.billing_adress_first_name'
        db.add_column('accounts_myprofile', 'billing_adress_first_name',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=80),
                      keep_default=False)

        # Adding field 'MyProfile.billing_adress_last_name'
        db.add_column('accounts_myprofile', 'billing_adress_last_name',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=80),
                      keep_default=False)

        # Adding field 'MyProfile.billing_adress_email'
        db.add_column('accounts_myprofile', 'billing_adress_email',
                      self.gf('django.db.models.fields.EmailField')(default=1, max_length=75),
                      keep_default=False)

        # Adding field 'MyProfile.billing_adress_phone'
        db.add_column('accounts_myprofile', 'billing_adress_phone',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=20),
                      keep_default=False)

        # Adding field 'MyProfile.billing_adress_street'
        db.add_column('accounts_myprofile', 'billing_adress_street',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=80),
                      keep_default=False)

        # Adding field 'MyProfile.billing_adress_city'
        db.add_column('accounts_myprofile', 'billing_adress_city',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=80),
                      keep_default=False)

        # Adding field 'MyProfile.billing_adress_postcode'
        db.add_column('accounts_myprofile', 'billing_adress_postcode',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=10),
                      keep_default=False)

        # Adding field 'MyProfile.billing_adress_country'
        db.add_column('accounts_myprofile', 'billing_adress_country',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=80),
                      keep_default=False)

        # Adding field 'MyProfile.shipping_adress_first_name'
        db.add_column('accounts_myprofile', 'shipping_adress_first_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=80, blank=True),
                      keep_default=False)

        # Adding field 'MyProfile.shipping_adress_last_name'
        db.add_column('accounts_myprofile', 'shipping_adress_last_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=80, blank=True),
                      keep_default=False)

        # Adding field 'MyProfile.shipping_adress_street'
        db.add_column('accounts_myprofile', 'shipping_adress_street',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=80, blank=True),
                      keep_default=False)

        # Adding field 'MyProfile.shipping_adress_city'
        db.add_column('accounts_myprofile', 'shipping_adress_city',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=80, blank=True),
                      keep_default=False)

        # Adding field 'MyProfile.shipping_adress_postcode'
        db.add_column('accounts_myprofile', 'shipping_adress_postcode',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=10, blank=True),
                      keep_default=False)

        # Adding field 'MyProfile.shipping_adress_country'
        db.add_column('accounts_myprofile', 'shipping_adress_country',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=80, blank=True),
                      keep_default=False)

        # Adding field 'MyProfile.additional_instructions'
        db.add_column('accounts_myprofile', 'additional_instructions',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'MyProfile.alternativ_shipping_adress'
        db.add_column('accounts_myprofile', 'alternativ_shipping_adress',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'MyProfile.billing_adress_first_name'
        db.delete_column('accounts_myprofile', 'billing_adress_first_name')

        # Deleting field 'MyProfile.billing_adress_last_name'
        db.delete_column('accounts_myprofile', 'billing_adress_last_name')

        # Deleting field 'MyProfile.billing_adress_email'
        db.delete_column('accounts_myprofile', 'billing_adress_email')

        # Deleting field 'MyProfile.billing_adress_phone'
        db.delete_column('accounts_myprofile', 'billing_adress_phone')

        # Deleting field 'MyProfile.billing_adress_street'
        db.delete_column('accounts_myprofile', 'billing_adress_street')

        # Deleting field 'MyProfile.billing_adress_city'
        db.delete_column('accounts_myprofile', 'billing_adress_city')

        # Deleting field 'MyProfile.billing_adress_postcode'
        db.delete_column('accounts_myprofile', 'billing_adress_postcode')

        # Deleting field 'MyProfile.billing_adress_country'
        db.delete_column('accounts_myprofile', 'billing_adress_country')

        # Deleting field 'MyProfile.shipping_adress_first_name'
        db.delete_column('accounts_myprofile', 'shipping_adress_first_name')

        # Deleting field 'MyProfile.shipping_adress_last_name'
        db.delete_column('accounts_myprofile', 'shipping_adress_last_name')

        # Deleting field 'MyProfile.shipping_adress_street'
        db.delete_column('accounts_myprofile', 'shipping_adress_street')

        # Deleting field 'MyProfile.shipping_adress_city'
        db.delete_column('accounts_myprofile', 'shipping_adress_city')

        # Deleting field 'MyProfile.shipping_adress_postcode'
        db.delete_column('accounts_myprofile', 'shipping_adress_postcode')

        # Deleting field 'MyProfile.shipping_adress_country'
        db.delete_column('accounts_myprofile', 'shipping_adress_country')

        # Deleting field 'MyProfile.additional_instructions'
        db.delete_column('accounts_myprofile', 'additional_instructions')

        # Deleting field 'MyProfile.alternativ_shipping_adress'
        db.delete_column('accounts_myprofile', 'alternativ_shipping_adress')


    models = {
        'accounts.myprofile': {
            'Meta': {'object_name': 'MyProfile'},
            'additional_instructions': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'alternativ_shipping_adress': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'billing_adress_city': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'billing_adress_country': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'billing_adress_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'billing_adress_first_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'billing_adress_last_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'billing_adress_phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'billing_adress_postcode': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'billing_adress_street': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mugshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'privacy': ('django.db.models.fields.CharField', [], {'default': "'registered'", 'max_length': '15'}),
            'shipping_adress_city': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'shipping_adress_country': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'shipping_adress_first_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'shipping_adress_last_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'shipping_adress_postcode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'shipping_adress_street': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'my_profile'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['accounts']