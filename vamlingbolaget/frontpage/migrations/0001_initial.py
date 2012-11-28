# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Frontpage'
        db.create_table('frontpage_frontpage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('body', self.gf('ckeditor.fields.RichTextField')()),
            ('extra_head', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('show_extra_head', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('frontpage', ['Frontpage'])


    def backwards(self, orm):
        # Deleting model 'Frontpage'
        db.delete_table('frontpage_frontpage')


    models = {
        'frontpage.frontpage': {
            'Meta': {'object_name': 'Frontpage'},
            'body': ('ckeditor.fields.RichTextField', [], {}),
            'extra_head': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'show_extra_head': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['frontpage']