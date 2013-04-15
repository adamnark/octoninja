# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'GpsUser'
        db.delete_table('gpsweb_gpsuser')


        # Changing field 'Driver.owner'
        db.alter_column('gpsweb_driver', 'owner_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'Car.owner'
        db.alter_column('gpsweb_car', 'owner_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'Unit.owner'
        db.alter_column('gpsweb_unit', 'owner_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

    def backwards(self, orm):
        # Adding model 'GpsUser'
        db.create_table('gpsweb_gpsuser', (
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gpsweb.Person'])),
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('gpsweb', ['GpsUser'])


        # Changing field 'Driver.owner'
        db.alter_column('gpsweb_driver', 'owner_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gpsweb.GpsUser']))

        # Changing field 'Car.owner'
        db.alter_column('gpsweb_car', 'owner_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gpsweb.GpsUser']))

        # Changing field 'Unit.owner'
        db.alter_column('gpsweb_unit', 'owner_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gpsweb.GpsUser']))

    models = {
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
        },
        'gpsweb.alert': {
            'Meta': {'object_name': 'Alert'},
            'car': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gpsweb.Car']"}),
            'cutoff': ('django.db.models.fields.IntegerField', [], {}),
            'geo_bottom_right_lat': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'geo_bottom_right_long': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'geo_top_left_lat': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'geo_top_left_long': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_speed': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'recipients': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['gpsweb.Person']", 'symmetrical': 'False'}),
            'schedule_bit_field': ('django.db.models.fields.CharField', [], {'max_length': '168'}),
            'state': ('django.db.models.fields.DateTimeField', [], {}),
            'type': ('django.db.models.fields.IntegerField', [], {'max_length': '1'})
        },
        'gpsweb.alertlog': {
            'Meta': {'object_name': 'AlertLog'},
            'alert': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gpsweb.Alert']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location_log': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gpsweb.LocationLog']"}),
            'marked_as_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'notification_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'gpsweb.car': {
            'Meta': {'object_name': 'Car'},
            'car_number': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'icon': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'primary_driver': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gpsweb.Driver']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
        },
        'gpsweb.driver': {
            'Meta': {'object_name': 'Driver'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gpsweb.Person']"})
        },
        'gpsweb.locationlog': {
            'Meta': {'object_name': 'LocationLog'},
            'car': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gpsweb.Car']"}),
            'heading': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'long': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'speed': ('django.db.models.fields.IntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        'gpsweb.person': {
            'Meta': {'object_name': 'Person'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        },
        'gpsweb.temporarydriver': {
            'Meta': {'object_name': 'TemporaryDriver'},
            'car': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gpsweb.Car']"}),
            'driver': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gpsweb.Driver']"}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        },
        'gpsweb.unit': {
            'Meta': {'object_name': 'Unit'},
            'car': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gpsweb.Car']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imei': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'sim_num': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        }
    }

    complete_apps = ['gpsweb']