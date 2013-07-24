# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'MediaFiles.description'
        db.alter_column(u'django_press_gallery_mediafiles', 'description', self.gf('django.db.models.fields.CharField')(default=' ', max_length=50))

        # Changing field 'MediaFiles.media_file'
        db.alter_column(u'django_press_gallery_mediafiles', 'media_file', self.gf('django_press_gallery.DPGImageField')(max_length=100))

    def backwards(self, orm):

        # Changing field 'MediaFiles.description'
        db.alter_column(u'django_press_gallery_mediafiles', 'description', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'MediaFiles.media_file'
        db.alter_column(u'django_press_gallery_mediafiles', 'media_file', self.gf('stdimage.fields.StdImageField')(max_length=100))

    models = {
        u'django_press_gallery.mediafiles': {
            'Meta': {'object_name': 'MediaFiles'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_press_gallery.MediaGroup']"}),
            'media_file': ('django_press_gallery.DPGImageField', [], {'max_length': '100'}),
            'media_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'django_press_gallery.mediagroup': {
            'Meta': {'object_name': 'MediaGroup'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mediaset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_press_gallery.MediaSet']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'django_press_gallery.mediaset': {
            'Meta': {'object_name': 'MediaSet'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['django_press_gallery']