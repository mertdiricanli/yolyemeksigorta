# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GooglePlusUser'
        db.create_table(u'web_googleplususer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('access_token', self.gf('django.db.models.fields.TextField')()),
            ('expiry_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('googleplus_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100, db_index=True)),
            ('googleplus_display_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100, db_index=True)),
        ))
        db.send_create_signal(u'web', ['GooglePlusUser'])

        # Adding model 'Company'
        db.create_table(u'web_company', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sector', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.Sector'])),
            ('companyname', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('companyslug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=200)),
        ))
        db.send_create_signal(u'web', ['Company'])

        # Adding model 'UserProfile'
        db.create_table(u'web_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal(u'web', ['UserProfile'])

        # Adding M2M table for field follows on 'UserProfile'
        m2m_table_name = db.shorten_name(u'web_userprofile_follows')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_userprofile', models.ForeignKey(orm[u'web.userprofile'], null=False)),
            ('to_userprofile', models.ForeignKey(orm[u'web.userprofile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_userprofile_id', 'to_userprofile_id'])

        # Adding model 'Sector'
        db.create_table(u'web_sector', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sectorname', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('sectorslug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=200)),
        ))
        db.send_create_signal(u'web', ['Sector'])

        # Adding model 'Category'
        db.create_table(u'web_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('categoryname', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('categoryslug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=200)),
        ))
        db.send_create_signal(u'web', ['Category'])

        # Adding model 'Post'
        db.create_table(u'web_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.Category'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.Company'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('timestamp', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'web', ['Post'])


    def backwards(self, orm):
        # Deleting model 'GooglePlusUser'
        db.delete_table(u'web_googleplususer')

        # Deleting model 'Company'
        db.delete_table(u'web_company')

        # Deleting model 'UserProfile'
        db.delete_table(u'web_userprofile')

        # Removing M2M table for field follows on 'UserProfile'
        db.delete_table(db.shorten_name(u'web_userprofile_follows'))

        # Deleting model 'Sector'
        db.delete_table(u'web_sector')

        # Deleting model 'Category'
        db.delete_table(u'web_category')

        # Deleting model 'Post'
        db.delete_table(u'web_post')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'web.category': {
            'Meta': {'object_name': 'Category'},
            'categoryname': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'categoryslug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'web.company': {
            'Meta': {'object_name': 'Company'},
            'companyname': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'companyslug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Sector']"})
        },
        u'web.googleplususer': {
            'Meta': {'object_name': 'GooglePlusUser'},
            'access_token': ('django.db.models.fields.TextField', [], {}),
            'expiry_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'googleplus_display_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'googleplus_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'web.post': {
            'Meta': {'object_name': 'Post'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Category']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Company']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'web.sector': {
            'Meta': {'object_name': 'Sector'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sectorname': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'sectorslug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'web.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'follows': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'followed_by'", 'symmetrical': 'False', 'to': u"orm['web.UserProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['web']