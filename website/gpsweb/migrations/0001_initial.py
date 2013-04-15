# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Person'
        db.create_table('gpsweb_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal('gpsweb', ['Person'])

        # Adding model 'GpsUser'
        db.create_table('gpsweb_gpsuser', (
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gpsweb.Person'])),
        ))
        db.send_create_signal('gpsweb', ['GpsUser'])

        # Adding model 'Driver'
        db.create_table('gpsweb_driver', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gpsweb.Person'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gpsweb.GpsUser'])),
        ))
        db.send_create_signal('gpsweb', ['Driver'])

        # Adding model 'Car'
        db.create_table('gpsweb_car', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('car_number', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gpsweb.GpsUser'])),
            ('primary_driver', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gpsweb.Driver'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('icon', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('gpsweb', ['Car'])

        # Adding model 'Unit'
        db.create_table('gpsweb_unit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('imei', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('sim_num', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gpsweb.GpsUser'])),
            ('car', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gpsweb.Car'], null=True, on_delete=models.SET_NULL, blank=True)),
        ))
        db.send_create_signal('gpsweb', ['Unit'])

        # Adding model 'TemporaryDriver'
        db.create_table('gpsweb_temporarydriver', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('driver', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gpsweb.Driver'])),
            ('car', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gpsweb.Car'])),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('gpsweb', ['TemporaryDriver'])

        # Adding model 'LocationLog'
        db.create_table('gpsweb_locationlog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('lat', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('long', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('speed', self.gf('django.db.models.fields.IntegerField')()),
            ('heading', self.gf('django.db.models.fields.IntegerField')()),
            ('car', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gpsweb.Car'])),
        ))
        db.send_create_signal('gpsweb', ['LocationLog'])

        # Adding model 'Alert'
        db.create_table('gpsweb_alert', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('car', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gpsweb.Car'])),
            ('state', self.gf('django.db.models.fields.DateTimeField')()),
            ('cutoff', self.gf('django.db.models.fields.IntegerField')()),
            ('type', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
            ('max_speed', self.gf('django.db.models.fields.IntegerField')()),
            ('schedule_bit_field', self.gf('django.db.models.fields.CharField')(max_length=168)),
            ('geo_top_left_lat', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('geo_top_left_long', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('geo_bottom_right_lat', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('geo_bottom_right_long', self.gf('django.db.models.fields.CharField')(max_length=13)),
        ))
        db.send_create_signal('gpsweb', ['Alert'])

        # Adding M2M table for field recipients on 'Alert'
        db.create_table('gpsweb_alert_recipients', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('alert', models.ForeignKey(orm['gpsweb.alert'], null=False)),
            ('person', models.ForeignKey(orm['gpsweb.person'], null=False))
        ))
        db.create_unique('gpsweb_alert_recipients', ['alert_id', 'person_id'])

        # Adding model 'AlertLog'
        db.create_table('gpsweb_alertlog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location_log', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gpsweb.LocationLog'])),
            ('alert', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gpsweb.Alert'])),
            ('notification_sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('marked_as_read', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('gpsweb', ['AlertLog'])


    def backwards(self, orm):
        # Deleting model 'Person'
        db.delete_table('gpsweb_person')

        # Deleting model 'GpsUser'
        db.delete_table('gpsweb_gpsuser')

        # Deleting model 'Driver'
        db.delete_table('gpsweb_driver')

        # Deleting model 'Car'
        db.delete_table('gpsweb_car')

        # Deleting model 'Unit'
        db.delete_table('gpsweb_unit')

        # Deleting model 'TemporaryDriver'
        db.delete_table('gpsweb_temporarydriver')

        # Deleting model 'LocationLog'
        db.delete_table('gpsweb_locationlog')

        # Deleting model 'Alert'
        db.delete_table('gpsweb_alert')

        # Removing M2M table for field recipients on 'Alert'
        db.delete_table('gpsweb_alert_recipients')

        # Deleting model 'AlertLog'
        db.delete_table('gpsweb_alertlog')


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
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gpsweb.GpsUser']"}),
            'primary_driver': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gpsweb.Driver']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
        },
        'gpsweb.driver': {
            'Meta': {'object_name': 'Driver'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gpsweb.GpsUser']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gpsweb.Person']"})
        },
        'gpsweb.gpsuser': {
            'Meta': {'object_name': 'GpsUser', '_ormbases': ['auth.User']},
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gpsweb.Person']"}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
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
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gpsweb.GpsUser']"}),
            'sim_num': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        }
    }

    complete_apps = ['gpsweb']