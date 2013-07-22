# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Media'
        db.delete_table(u'django_press_gallery_media')

        # Adding model 'MediaGroup'
        db.create_table(u'django_press_gallery_mediagroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('mediaset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_press_gallery.MediaSet'])),
        ))
        db.send_create_signal(u'django_press_gallery', ['MediaGroup'])

        # Deleting field 'MediaFiles.parent_media'
        db.delete_column(u'django_press_gallery_mediafiles', 'parent_media_id')

        # Adding field 'MediaFiles.media'
        db.add_column(u'django_press_gallery_mediafiles', 'media',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['django_press_gallery.MediaGroup']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Media'
        db.create_table(u'django_press_gallery_media', (
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('mediaset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_press_gallery.MediaSet'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'django_press_gallery', ['Media'])

        # Deleting model 'MediaGroup'
        db.delete_table(u'django_press_gallery_mediagroup')

        # Adding field 'MediaFiles.parent_media'
        db.add_column(u'django_press_gallery_mediafiles', 'parent_media',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_press_gallery.MediaFiles'], null=True, blank=True),
                      keep_default=False)

        # Deleting field 'MediaFiles.media'
        db.delete_column(u'django_press_gallery_mediafiles', 'media_id')


    models = {
        u'django_press_gallery.mediafiles': {
            'Meta': {'object_name': 'MediaFiles'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_press_gallery.MediaGroup']"}),
            'media_file': ('stdimage.fields.StdImageField', [], {'max_length': '100'}),
            'media_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'mediaset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_press_gallery.MediaSet']"}),
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