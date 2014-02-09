# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Tractor.name'
        db.alter_column(u'backend_tractor', 'name', self.gf('django.db.models.fields.CharField')(max_length=100))

    def backwards(self, orm):

        # Changing field 'Tractor.name'
        db.alter_column(u'backend_tractor', 'name', self.gf('django.db.models.fields.CharField')(max_length=200))

    models = {
        u'backend.tractor': {
            'Meta': {'object_name': 'Tractor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['backend']