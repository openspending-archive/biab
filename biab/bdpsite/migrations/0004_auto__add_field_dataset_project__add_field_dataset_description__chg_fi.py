# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Dataset.project'
        db.add_column(u'bdpsite_dataset', 'project',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['bdpsite.Project']),
                      keep_default=False)

        # Adding field 'Dataset.description'
        db.add_column(u'bdpsite_dataset', 'description',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


        # Changing field 'Dataset.status'
        db.alter_column(u'bdpsite_dataset', 'status', self.gf('django.db.models.fields.CharField')(max_length=256, null=True))

        # Changing field 'Dataset.datapackage'
        db.alter_column(u'bdpsite_dataset', 'datapackage_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bdpsite.DataPackage'], null=True))

        # Changing field 'Dataset.granularity'
        db.alter_column(u'bdpsite_dataset', 'granularity', self.gf('django.db.models.fields.CharField')(max_length=256, null=True))

        # Changing field 'Dataset.path'
        db.alter_column(u'bdpsite_dataset', 'path', self.gf('django.db.models.fields.CharField')(max_length=256, null=True))

        # Changing field 'Dataset.fiscalYear'
        db.alter_column(u'bdpsite_dataset', 'fiscalYear', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):
        # Deleting field 'Dataset.project'
        db.delete_column(u'bdpsite_dataset', 'project_id')

        # Deleting field 'Dataset.description'
        db.delete_column(u'bdpsite_dataset', 'description')


        # Changing field 'Dataset.status'
        db.alter_column(u'bdpsite_dataset', 'status', self.gf('django.db.models.fields.CharField')(default=1, max_length=256))

        # User chose to not deal with backwards NULL issues for 'Dataset.datapackage'
        raise RuntimeError("Cannot reverse this migration. 'Dataset.datapackage' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Dataset.datapackage'
        db.alter_column(u'bdpsite_dataset', 'datapackage_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bdpsite.DataPackage']))

        # User chose to not deal with backwards NULL issues for 'Dataset.granularity'
        raise RuntimeError("Cannot reverse this migration. 'Dataset.granularity' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Dataset.granularity'
        db.alter_column(u'bdpsite_dataset', 'granularity', self.gf('django.db.models.fields.CharField')(max_length=256))

        # User chose to not deal with backwards NULL issues for 'Dataset.path'
        raise RuntimeError("Cannot reverse this migration. 'Dataset.path' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Dataset.path'
        db.alter_column(u'bdpsite_dataset', 'path', self.gf('django.db.models.fields.CharField')(max_length=256))

        # User chose to not deal with backwards NULL issues for 'Dataset.fiscalYear'
        raise RuntimeError("Cannot reverse this migration. 'Dataset.fiscalYear' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Dataset.fiscalYear'
        db.alter_column(u'bdpsite_dataset', 'fiscalYear', self.gf('django.db.models.fields.DateTimeField')())

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'bdpsite.datapackage': {
            'Meta': {'object_name': 'DataPackage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bdpsite.Project']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'bdpsite.dataset': {
            'Meta': {'object_name': 'Dataset'},
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'datapackage': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bdpsite.DataPackage']", 'null': 'True', 'blank': 'True'}),
            'dateLastUpdated': ('django.db.models.fields.DateTimeField', [], {}),
            'datePublished': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fiscalYear': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'granularity': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bdpsite.Project']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'bdpsite.project': {
            'Meta': {'object_name': 'Project'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'bdpsite.visualization': {
            'Meta': {'object_name': 'Visualization'},
            'dataset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bdpsite.Dataset']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['bdpsite']